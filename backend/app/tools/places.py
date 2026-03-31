"""
Google Places API (New v1) + Geocoding API wrappers.

Key differences from the legacy Places API:
- Nearby Search: POST /v1/places:searchNearby (JSON body, not GET params)
- Place Details: GET /v1/places/{place_id} with X-Goog-FieldMask header
- Text Search:   POST /v1/places:searchText
- priceLevel:    Returns enum strings (PRICE_LEVEL_MODERATE etc.), not integers
"""
from app.core.config import settings
from app.core.clients import get_http_client
from app.utils.logger import get_logger

logger = get_logger(__name__)

_PRICE_LEVEL_MAP = {
    "PRICE_LEVEL_FREE": 0,
    "PRICE_LEVEL_INEXPENSIVE": 1,
    "PRICE_LEVEL_MODERATE": 2,
    "PRICE_LEVEL_EXPENSIVE": 3,
    "PRICE_LEVEL_VERY_EXPENSIVE": 4,
}


def _parse_price_level(raw: str | None) -> int | None:
    if raw is None:
        return None
    return _PRICE_LEVEL_MAP.get(raw)


async def geocode_address(address: str) -> dict:
    """Returns {"lat": float, "lng": float, "formatted_address": str}"""
    client = get_http_client()
    resp = await client.get(
        settings.geocoding_base_url,
        params={"address": address, "key": settings.google_places_api_key},
    )
    resp.raise_for_status()
    data = resp.json()
    if data["status"] != "OK":
        raise ValueError(f"Geocoding failed: {data['status']} — {data.get('error_message', '')}")
    result = data["results"][0]
    loc = result["geometry"]["location"]
    return {
        "lat": loc["lat"],
        "lng": loc["lng"],
        "formatted_address": result["formatted_address"],
    }


async def nearby_search(
    lat: float,
    lng: float,
    business_type: str,
    radius_meters: int = 1000,
    max_results: int = 20,
) -> list[dict]:
    """
    POST https://places.googleapis.com/v1/places:searchNearby
    Returns list of simplified place dicts.
    """
    client = get_http_client()
    body = {
        "includedTypes": [business_type],
        "maxResultCount": min(max_results, 20),
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": float(radius_meters),
            }
        },
    }
    resp = await client.post(
        f"{settings.places_base_url}/places:searchNearby",
        json=body,
        headers={
            "X-Goog-Api-Key": settings.google_places_api_key,
            "X-Goog-FieldMask": (
                "places.id,places.displayName,places.formattedAddress,"
                "places.rating,places.userRatingCount,places.priceLevel,"
                "places.location,places.types"
            ),
        },
    )
    resp.raise_for_status()
    places = resp.json().get("places", [])
    return [_normalize_place(p) for p in places]


async def place_details(place_id: str, fields: list[str] | None = None) -> dict:
    """
    GET https://places.googleapis.com/v1/places/{place_id}
    """
    if fields is None:
        fields = [
            "rating",
            "reviews",
            "currentOpeningHours",
            "priceLevel",
            "userRatingCount",
            "displayName",
            "formattedAddress",
            "types",
            "location",
        ]
    client = get_http_client()
    # The place_id from nearby_search may be just the ID or the full resource name
    resource_name = place_id if place_id.startswith("places/") else place_id
    resp = await client.get(
        f"{settings.places_base_url}/{resource_name}",
        headers={
            "X-Goog-Api-Key": settings.google_places_api_key,
            "X-Goog-FieldMask": ",".join(fields),
        },
    )
    resp.raise_for_status()
    data = resp.json()
    return _normalize_place(data)


async def text_search(
    query: str,
    lat: float,
    lng: float,
    radius_meters: int = 1500,
) -> list[dict]:
    """
    POST https://places.googleapis.com/v1/places:searchText
    """
    client = get_http_client()
    body = {
        "textQuery": query,
        "locationBias": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": float(radius_meters),
            }
        },
        "maxResultCount": 20,
    }
    resp = await client.post(
        f"{settings.places_base_url}/places:searchText",
        json=body,
        headers={
            "X-Goog-Api-Key": settings.google_places_api_key,
            "X-Goog-FieldMask": (
                "places.id,places.displayName,places.formattedAddress,"
                "places.rating,places.userRatingCount,places.priceLevel,"
                "places.types,places.location"
            ),
        },
    )
    resp.raise_for_status()
    places = resp.json().get("places", [])
    return [_normalize_place(p) for p in places]


def _normalize_place(p: dict) -> dict:
    """Flatten nested Places API v1 structure into a flat dict."""
    loc = p.get("location", {})
    display_name = p.get("displayName", {})
    return {
        "place_id": p.get("id", p.get("name", "")),
        "name": display_name.get("text", "") if isinstance(display_name, dict) else display_name,
        "address": p.get("formattedAddress", ""),
        "lat": loc.get("latitude", 0.0),
        "lng": loc.get("longitude", 0.0),
        "rating": p.get("rating"),
        "user_ratings_total": p.get("userRatingCount", 0),
        "price_level": _parse_price_level(p.get("priceLevel")),
        "types": p.get("types", []),
        "opening_hours": p.get("currentOpeningHours", {}),
        "reviews": p.get("reviews", []),
    }
