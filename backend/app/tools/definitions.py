# ---------------------------------------------------------------------------
# Tool schemas for sub-agents (Google Places tools)
# ---------------------------------------------------------------------------

GEOCODE_ADDRESS = {
    "name": "geocode_address",
    "description": "Convert a human-readable address into latitude/longitude coordinates.",
    "input_schema": {
        "type": "object",
        "properties": {
            "address": {
                "type": "string",
                "description": "Full address to geocode, e.g. '123 Main St, London, UK'",
            }
        },
        "required": ["address"],
    },
}

NEARBY_SEARCH = {
    "name": "nearby_search",
    "description": (
        "Search for businesses of a given type near a lat/lng coordinate "
        "using Google Places Nearby Search. Returns a list of places."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "lat": {"type": "number", "description": "Latitude of the search center"},
            "lng": {"type": "number", "description": "Longitude of the search center"},
            "business_type": {
                "type": "string",
                "description": (
                    "Google Places type string, e.g. 'cafe', 'gym', 'restaurant', "
                    "'supermarket', 'transit_station', 'park'"
                ),
            },
            "radius_meters": {
                "type": "integer",
                "description": "Search radius in meters (default 1000)",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return (max 20)",
            },
        },
        "required": ["lat", "lng", "business_type"],
    },
}

PLACE_DETAILS = {
    "name": "place_details",
    "description": (
        "Get detailed information about a specific place including reviews, "
        "opening hours, price level, and rating."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "place_id": {
                "type": "string",
                "description": "The place ID returned by nearby_search or text_search",
            },
            "fields": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Fields to fetch. Available: rating, reviews, currentOpeningHours, "
                    "priceLevel, userRatingCount, displayName, formattedAddress, types"
                ),
            },
        },
        "required": ["place_id"],
    },
}

TEXT_SEARCH = {
    "name": "text_search",
    "description": "Search for businesses using a free-text query near a location.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query, e.g. 'specialty coffee Shoreditch' or 'vegan cafe'",
            },
            "lat": {"type": "number"},
            "lng": {"type": "number"},
            "radius_meters": {
                "type": "integer",
                "description": "Search radius in meters (default 1500)",
            },
        },
        "required": ["query", "lat", "lng"],
    },
}

# ---------------------------------------------------------------------------
# Orchestrator-level tool schemas (invoke sub-agents)
# ---------------------------------------------------------------------------

RUN_COMPETITOR_ANALYSIS = {
    "name": "run_competitor_analysis",
    "description": (
        "Run the Competitor Agent to find and score all nearby competitors "
        "for the target business type at the given coordinates."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "lat": {"type": "number"},
            "lng": {"type": "number"},
            "business_type": {"type": "string"},
            "radius_meters": {"type": "integer"},
        },
        "required": ["lat", "lng", "business_type", "radius_meters"],
    },
}

RUN_LOCATION_SCORING = {
    "name": "run_location_scoring",
    "description": (
        "Run the Location Agent to produce a 0-100 suitability score "
        "for the target coordinates."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "lat": {"type": "number"},
            "lng": {"type": "number"},
            "business_type": {"type": "string"},
            "radius_meters": {"type": "integer"},
        },
        "required": ["lat", "lng", "business_type", "radius_meters"],
    },
}

RUN_TRAFFIC_ESTIMATION = {
    "name": "run_traffic_estimation",
    "description": (
        "Run the Traffic Agent to estimate foot traffic and demand "
        "at the target location."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "lat": {"type": "number"},
            "lng": {"type": "number"},
            "business_type": {"type": "string"},
            "radius_meters": {"type": "integer"},
        },
        "required": ["lat", "lng", "business_type", "radius_meters"],
    },
}

RUN_GAP_ANALYSIS = {
    "name": "run_gap_analysis",
    "description": (
        "Run the Gap Agent to identify market gaps and underserved "
        "opportunities near the target location."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "lat": {"type": "number"},
            "lng": {"type": "number"},
            "business_type": {"type": "string"},
            "radius_meters": {"type": "integer"},
        },
        "required": ["lat", "lng", "business_type", "radius_meters"],
    },
}
