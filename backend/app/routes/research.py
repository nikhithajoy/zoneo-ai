from fastapi import APIRouter, HTTPException
from app.schemas.report import (
    ResearchRequest,
    ResearchResponse,
    CompetitorOut,
    LocationScoreOut,
    TrafficEstimateOut,
    MarketGapOut,
)
from app.services.research_service import run_research
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    """
    Run the full market research pipeline for a given address and business type.

    - Geocodes the address
    - Runs competitor analysis, location scoring, traffic estimation, and gap analysis in parallel
    - Returns a structured market research report
    """
    try:
        report = await run_research(
            address=request.address,
            business_type=request.business_type,
            radius_meters=request.radius_meters,
            max_competitors=request.max_competitors,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        logger.error("Research pipeline failed: %s", exc)
        raise HTTPException(status_code=500, detail=f"Pipeline error: {exc}")

    return ResearchResponse(
        request_address=report.request_address,
        request_business_type=report.request_business_type,
        executive_summary=report.executive_summary,
        competitors=[
            CompetitorOut(
                name=c.name,
                address=c.address,
                rating=c.rating,
                user_ratings_total=c.user_ratings_total,
                price_level=c.price_level,
                distance_meters=c.distance_meters,
                competitive_score=c.competitive_score,
            )
            for c in report.competitors
        ],
        location_score=LocationScoreOut(
            overall=report.location_score.overall,
            competition_density=report.location_score.competition_density,
            accessibility_proxy=report.location_score.accessibility_proxy,
            demand_signal=report.location_score.demand_signal,
            notes=report.location_score.notes,
        ),
        traffic_estimate=TrafficEstimateOut(
            busy_hours_summary=report.traffic_estimate.busy_hours_summary,
            peak_day=report.traffic_estimate.peak_day,
            estimated_daily_footfall=report.traffic_estimate.estimated_daily_footfall,
            confidence=report.traffic_estimate.confidence,
            reasoning=report.traffic_estimate.reasoning,
        ),
        market_gaps=[
            MarketGapOut(
                gap_type=g.gap_type,
                description=g.description,
                opportunity_score=g.opportunity_score,
                supporting_evidence=g.supporting_evidence,
            )
            for g in report.market_gaps
        ],
        recommendations=report.recommendations,
    )


@router.get("/health")
def health():
    return {"status": "ok"}
