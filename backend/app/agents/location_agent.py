from app.agents.base import BaseAgent
from app.tools.definitions import NEARBY_SEARCH, TEXT_SEARCH, GEOCODE_ADDRESS
from app.prompts.location import LOCATION_SYSTEM_PROMPT


class LocationAgent(BaseAgent):
    """
    Scores the target location for suitability across three dimensions:
    competition density, accessibility, and demand signal.
    Returns a JSON LocationScore object.
    """

    system_prompt = LOCATION_SYSTEM_PROMPT
    tools = [NEARBY_SEARCH, TEXT_SEARCH, GEOCODE_ADDRESS]
