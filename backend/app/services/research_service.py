"""
Top-level pipeline entry point.
Invokes the OrchestratorAgent and parses its JSON output into typed domain objects.
"""
import json
from app.agents.orchestrator import OrchestratorAgent
from app.schemas.report import (
    MarketResearchReport,
    Competitor,
    LocationScore,
    TrafficEstimate,
    MarketGap,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _extract_json(text: str) -> str:
    """Extract JSON from Claude output, handling prose before/after and markdown fences."""
    import re
    text = text.strip()
    # Try to extract from ```json ... ``` or ``` ... ``` fence
    match = re.search(r'```(?:json)?\s*\n([\s\S]*?)\n```', text)
    if match:
        return match.group(1).strip()
    # Fall back: find first { to last }
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return text


async def run_research(
    address: str,
    business_type: str,
    radius_meters: int = 1000,
    max_competitors: int = 20,
) -> MarketResearchReport:
    """
    Run the full multi-agent market research pipeline.
    Returns a typed MarketResearchReport.
    """
    task = (
        f"Conduct a full market research analysis.\n"
        f"Address: {address}\n"
        f"Business type: {business_type}\n"
        f"Search radius: {radius_meters} meters\n"
        f"Max competitors to analyze: {max_competitors}"
    )

    logger.info("Starting market research pipeline: address=%r, type=%r", address, business_type)
    orchestrator = OrchestratorAgent()
    raw_output = await orchestrator.run(task)
    logger.info("Orchestrator complete. Parsing output...")

    cleaned = _extract_json(raw_output)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse orchestrator output: %s\nRaw output: %s", exc, raw_output[:500])
        raise ValueError(f"Orchestrator returned invalid JSON: {exc}") from exc

    competitors = [
        Competitor(
            place_id=c.get("place_id", ""),
            name=c.get("name", ""),
            address=c.get("address", ""),
            lat=float(c.get("lat", 0.0)),
            lng=float(c.get("lng", 0.0)),
            rating=c.get("rating"),
            user_ratings_total=int(c.get("user_ratings_total", 0)),
            price_level=c.get("price_level"),
            business_type=c.get("business_type", business_type),
            distance_meters=float(c.get("distance_meters", 0.0)),
            competitive_score=float(c.get("competitive_score", 0.0)),
        )
        for c in data.get("competitors", [])
    ]

    ls = data.get("location_score", {})
    location_score = LocationScore(
        overall=float(ls.get("overall", 0.0)),
        competition_density=float(ls.get("competition_density", 0.0)),
        accessibility_proxy=float(ls.get("accessibility_proxy", 0.0)),
        demand_signal=float(ls.get("demand_signal", 0.0)),
        notes=ls.get("notes", []),
    )

    te = data.get("traffic_estimate", {})
    traffic_estimate = TrafficEstimate(
        busy_hours_summary=te.get("busy_hours_summary", ""),
        peak_day=te.get("peak_day", ""),
        estimated_daily_footfall=te.get("estimated_daily_footfall", ""),
        confidence=te.get("confidence", ""),
        reasoning=te.get("reasoning", ""),
    )

    market_gaps = [
        MarketGap(
            gap_type=g.get("gap_type", ""),
            description=g.get("description", ""),
            opportunity_score=float(g.get("opportunity_score", 0.0)),
            supporting_evidence=g.get("supporting_evidence", []),
        )
        for g in data.get("market_gaps", [])
    ]

    report = MarketResearchReport(
        request_address=address,
        request_business_type=business_type,
        lat=0.0,
        lng=0.0,
        executive_summary=data.get("executive_summary", ""),
        competitors=competitors,
        location_score=location_score,
        traffic_estimate=traffic_estimate,
        market_gaps=market_gaps,
        recommendations=data.get("recommendations", []),
    )

    logger.info(
        "Report assembled: %d competitors, location_score=%.1f, %d gaps, %d recommendations",
        len(competitors),
        location_score.overall,
        len(market_gaps),
        len(report.recommendations),
    )
    return report
