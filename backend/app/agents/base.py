"""
BaseAgent: reusable Anthropic tool-calling agentic loop.
All specialist sub-agents inherit from this class.
"""
import asyncio
from anthropic import Anthropic
from anthropic.types import Message
from app.core.config import settings
from app.core.clients import get_anthropic_client
from app.tools.registry import dispatch
from app.utils.logger import get_logger

logger = get_logger(__name__)


class BaseAgent:
    """
    An agent that runs the Anthropic tool-calling loop until stop_reason == "end_turn".
    Subclasses set `system_prompt` and `tools` as class attributes.
    """

    system_prompt: str = ""
    tools: list[dict] = []

    def __init__(self) -> None:
        self.client: Anthropic = get_anthropic_client()

    async def run(self, user_message: str) -> str:
        """
        Run the agentic tool-calling loop for a single task.
        Returns the final text reply from Claude.
        """
        messages: list[dict] = [{"role": "user", "content": user_message}]

        while True:
            logger.info("[%s] Calling Claude (messages=%d)...", self.__class__.__name__, len(messages))

            # messages.create is synchronous — wrap in thread for async compatibility
            response: Message = await asyncio.to_thread(
                self.client.messages.create,
                model=settings.claude_model,
                max_tokens=settings.max_tokens,
                system=self.system_prompt,
                tools=self.tools,
                messages=messages,
            )

            logger.info("[%s] stop_reason=%s", self.__class__.__name__, response.stop_reason)

            if response.stop_reason == "end_turn":
                return next(
                    (b.text for b in response.content if hasattr(b, "text")), ""
                )

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result_str = await dispatch(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result_str,
                        })
                messages.append({"role": "user", "content": tool_results})

            else:
                # max_tokens or unexpected stop — return whatever text is available
                return next(
                    (b.text for b in response.content if hasattr(b, "text")), ""
                )
