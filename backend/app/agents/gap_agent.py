from app.agents.base import BaseAgent
from app.tools.definitions import NEARBY_SEARCH, TEXT_SEARCH, PLACE_DETAILS
from app.prompts.gap import GAP_SYSTEM_PROMPT


class GapAgent(BaseAgent):
    """
    Identifies market gaps by searching for adjacent or underrepresented
    business types near the target location.
    Returns a JSON array of MarketGap objects.
    """

    system_prompt = GAP_SYSTEM_PROMPT
    tools = [NEARBY_SEARCH, TEXT_SEARCH, PLACE_DETAILS]
