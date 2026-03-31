"""
Tool dispatcher for sub-agents (CompetitorAgent, LocationAgent, TrafficAgent, GapAgent).
Maps Claude tool_use block names to the Places API coroutines.
"""
import json
from app.tools import places
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def dispatch(name: str, inputs: dict) -> str:
    """
    Execute a tool by name and return its result as a JSON string.
    (Anthropic tool_result content must be a string.)
    """
    logger.info("Tool dispatch: %s | inputs: %s", name, str(inputs)[:200])
    try:
        if name == "geocode_address":
            result = await places.geocode_address(inputs["address"])

        elif name == "nearby_search":
            result = await places.nearby_search(
                lat=inputs["lat"],
                lng=inputs["lng"],
                business_type=inputs["business_type"],
                radius_meters=inputs.get("radius_meters", 1000),
                max_results=inputs.get("max_results", 20),
            )

        elif name == "place_details":
            result = await places.place_details(
                place_id=inputs["place_id"],
                fields=inputs.get("fields"),
            )

        elif name == "text_search":
            result = await places.text_search(
                query=inputs["query"],
                lat=inputs["lat"],
                lng=inputs["lng"],
                radius_meters=inputs.get("radius_meters", 1500),
            )

        else:
            result = {"error": f"Unknown tool: {name}"}

    except Exception as exc:
        logger.error("Tool error (%s): %s", name, exc)
        result = {"error": str(exc)}

    serialized = json.dumps(result)
    logger.info("Tool result (%s): %s...", name, serialized[:300])
    return serialized
