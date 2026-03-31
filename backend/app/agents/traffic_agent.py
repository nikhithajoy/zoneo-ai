from app.agents.base import BaseAgent
from app.tools.definitions import NEARBY_SEARCH, PLACE_DETAILS
from app.prompts.traffic import TRAFFIC_SYSTEM_PROMPT


class TrafficAgent(BaseAgent):
    """
    Estimates foot traffic and demand at the target location by analyzing
    competitor opening hours and review data.
    Returns a JSON TrafficEstimate object.
    """

    system_prompt = TRAFFIC_SYSTEM_PROMPT
    tools = [NEARBY_SEARCH, PLACE_DETAILS]
