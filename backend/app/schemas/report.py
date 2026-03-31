from dataclasses import dataclass, field
from typing import Optional
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Internal domain models (used between agents and the service layer)
# ---------------------------------------------------------------------------

@dataclass
class Competitor:
    place_id: str
    name: str
    address: str
    lat: float
    lng: float
    rating: Optional[float]
    user_ratings_total: int
    price_level: Optional[int]   # 0-4
    business_type: str
    distance_meters: float
    competitive_score: float     # 0-100


@dataclass
class LocationScore:
    overall: float               # 0-100
    competition_density: float   # 0=overcrowded, 100=clear market
    accessibility_proxy: float   # transit/footfall anchors nearby
    demand_signal: float         # validated demand from area reviews
    notes: list[str] = field(default_factory=list)


@dataclass
class TrafficEstimate:
    busy_hours_summary: str
    peak_day: str
    estimated_daily_footfall: str  # "low" | "medium" | "high"
    confidence: str                # "low" | "medium" | "high"
    reasoning: str


@dataclass
class MarketGap:
    gap_type: str
    description: str
    opportunity_score: float       # 0-100
    supporting_evidence: list[str] = field(default_factory=list)


@dataclass
class MarketResearchReport:
    request_address: str
    request_business_type: str
    lat: float
    lng: float
    executive_summary: str
    competitors: list[Competitor]
    location_score: LocationScore
    traffic_estimate: TrafficEstimate
    market_gaps: list[MarketGap]
    recommendations: list[str]


# ---------------------------------------------------------------------------
# API models (FastAPI request / response schemas)
# ---------------------------------------------------------------------------

class ResearchRequest(BaseModel):
    address: str
    business_type: str        # e.g. "coffee shop", "gym", "restaurant"
    radius_meters: int = 1000
    max_competitors: int = 20


class CompetitorOut(BaseModel):
    name: str
    address: str
    rating: Optional[float]
    user_ratings_total: int
    price_level: Optional[int]
    distance_meters: float
    competitive_score: float


class LocationScoreOut(BaseModel):
    overall: float
    competition_density: float
    accessibility_proxy: float
    demand_signal: float
    notes: list[str]


class TrafficEstimateOut(BaseModel):
    busy_hours_summary: str
    peak_day: str
    estimated_daily_footfall: str
    confidence: str
    reasoning: str


class MarketGapOut(BaseModel):
    gap_type: str
    description: str
    opportunity_score: float
    supporting_evidence: list[str]


class ResearchResponse(BaseModel):
    request_address: str
    request_business_type: str
    executive_summary: str
    competitors: list[CompetitorOut]
    location_score: LocationScoreOut
    traffic_estimate: TrafficEstimateOut
    market_gaps: list[MarketGapOut]
    recommendations: list[str]
