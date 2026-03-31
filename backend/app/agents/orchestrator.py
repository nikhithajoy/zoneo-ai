"""
OrchestratorAgent: coordinates the full market research pipeline.

Overrides BaseAgent.run() to use sub-agent dispatch instead of the Places API
tool registry. When Claude issues multiple tool_use blocks in one turn (which it
will for the 4 parallel sub-agent calls), asyncio.gather runs them concurrently.
"""
import asyncio
import json
from anthropic.types import Message
from app.agents.base import BaseAgent
from app.agents.competitor_agent import CompetitorAgent
from app.agents.location_agent import LocationAgent
from app.agents.traffic_agent import TrafficAgent
from app.agents.gap_agent import GapAgent
from app.tools.definitions import (
    GEOCODE_ADDRESS,
    RUN_COMPETITOR_ANALYSIS,
    RUN_LOCATION_SCORING,
    RUN_TRAFFIC_ESTIMATION,
    RUN_GAP_ANALYSIS,
)
from app.tools.places import geocode_address
from app.prompts.orchestrator import ORCHESTRATOR_SYSTEM_PROMPT
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OrchestratorAgent(BaseAgent):
    system_prompt = ORCHESTRATOR_SYSTEM_PROMPT
    tools = [
        GEOCODE_ADDRESS,
        RUN_COMPETITOR_ANALYSIS,
        RUN_LOCATION_SCORING,
        RUN_TRAFFIC_ESTIMATION,
        RUN_GAP_ANALYSIS,
    ]

    async def _dispatch_tool(self, name: str, inputs: dict) -> str:
        """Handle orchestrator-level tool calls (geocoding + sub-agent invocations)."""
        logger.info("[Orchestrator] Tool call: %s | inputs: %s", name, str(inputs)[:200])

        if name == "geocode_address":
            result = await geocode_address(inputs["address"])
            return json.dumps(result)

        lat = inputs["lat"]
        lng = inputs["lng"]
        btype = inputs["business_type"]
        radius = inputs.get("radius_meters", 1000)
        task_msg = (
            f"Analyze for a {btype} at lat={lat}, lng={lng}, radius={radius}m. "
            f"Return structured JSON only with no additional prose."
        )

        if name == "run_competitor_analysis":
            result = await CompetitorAgent().run(task_msg)
        elif name == "run_location_scoring":
            result = await LocationAgent().run(task_msg)
        elif name == "run_traffic_estimation":
            result = await TrafficAgent().run(task_msg)
        elif name == "run_gap_analysis":
            result = await GapAgent().run(task_msg)
        else:
            result = json.dumps({"error": f"Unknown orchestrator tool: {name}"})

        logger.info("[Orchestrator] Sub-agent %s complete. Result[:200]: %s", name, str(result)[:200])
        return result if isinstance(result, str) else json.dumps(result)

    async def run(self, user_message: str) -> str:
        """
        Override to use orchestrator tool dispatch and parallel sub-agent execution.
        """
        messages: list[dict] = [{"role": "user", "content": user_message}]

        while True:
            logger.info("[Orchestrator] Calling Claude (messages=%d)...", len(messages))

            response: Message = await asyncio.to_thread(
                self.client.messages.create,
                model=settings.claude_model,
                max_tokens=settings.max_tokens,
                system=self.system_prompt,
                tools=self.tools,
                messages=messages,
            )

            logger.info("[Orchestrator] stop_reason=%s", response.stop_reason)

            if response.stop_reason == "end_turn":
                return next(
                    (b.text for b in response.content if hasattr(b, "text")), ""
                )

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})

                tool_blocks = [b for b in response.content if b.type == "tool_use"]
                logger.info("[Orchestrator] Running %d tool(s) in parallel: %s",
                            len(tool_blocks), [b.name for b in tool_blocks])

                # Run all tool calls concurrently (key for parallel sub-agent execution)
                results = await asyncio.gather(*[
                    self._dispatch_tool(b.name, b.input)
                    for b in tool_blocks
                ])

                tool_results = [
                    {
                        "type": "tool_result",
                        "tool_use_id": b.id,
                        "content": r,
                    }
                    for b, r in zip(tool_blocks, results)
                ]
                messages.append({"role": "user", "content": tool_results})

            else:
                return next(
                    (b.text for b in response.content if hasattr(b, "text")), ""
                )
