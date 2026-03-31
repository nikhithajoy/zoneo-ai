from app.agents.base import BaseAgent
from app.tools.definitions import NEARBY_SEARCH, PLACE_DETAILS, TEXT_SEARCH
from app.prompts.competitor import COMPETITOR_SYSTEM_PROMPT


class CompetitorAgent(BaseAgent):
    """
    Finds and scores all nearby competitors using Google Places API.
    Returns a JSON array of Competitor objects.
    """

    system_prompt = COMPETITOR_SYSTEM_PROMPT
    tools = [NEARBY_SEARCH, PLACE_DETAILS, TEXT_SEARCH]
