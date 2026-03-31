# Market Research Agent

A full-stack AI-powered market research tool that performs competitive analysis for any location and business type. Enter an address and business type, and a multi-agent pipeline built on Claude and Google Places API returns a structured report covering competitors, location suitability, foot traffic estimates, and market opportunities.

![Demo](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/python-3.11+-blue) ![Next.js](https://img.shields.io/badge/next.js-16-black) ![License](https://img.shields.io/badge/license-MIT-blue)

---

## How It Works

1. **Geocode** — the address is resolved to coordinates via the Google Geocoding API
2. **Parallel sub-agents** — four specialist Claude agents run concurrently via `asyncio.gather()`:
   - **Competitor Agent** — finds and scores nearby businesses by rating, review volume, distance, and price level
   - **Location Agent** — scores suitability across competition density, accessibility, and demand signals (0–100)
   - **Traffic Agent** — estimates foot traffic from review patterns and opening hours
   - **Gap Agent** — identifies underserved market opportunities in the area
3. **Synthesis** — the Orchestrator agent combines all four outputs into a final structured report
4. **Display** — the Next.js frontend renders the report as an interactive dashboard

All agents output **JSON only**, making parsing deterministic and reliable.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS, Recharts |
| Backend | Python 3.11+, FastAPI, uvicorn |
| AI | Claude Sonnet 4.6 (Anthropic API) |
| Places Data | Google Places API (Nearby Search, Text Search, Place Details, Geocoding) |
| HTTP Client | httpx (async) |

---

## Project Structure

```
market-research-agent/
├── backend/
│   └── app/
│       ├── agents/             # Agentic loop implementations
│       │   ├── base.py         # BaseAgent (reusable tool-calling loop)
│       │   ├── orchestrator.py # Coordinates all sub-agents
│       │   ├── competitor_agent.py
│       │   ├── location_agent.py
│       │   ├── traffic_agent.py
│       │   └── gap_agent.py
│       ├── prompts/            # System prompts for each agent
│       ├── tools/              # Tool schemas, dispatcher, Places API wrapper
│       ├── services/           # Top-level pipeline (research_service.py)
│       ├── routes/             # FastAPI endpoints
│       ├── schemas/            # Pydantic models
│       ├── core/               # Config, API clients
│       └── main.py             # App init, CORS
│
├── frontend/
│   ├── app/                    # Next.js app router pages
│   ├── components/             # Dashboard, CompetitorTable, ScoreRing, etc.
│   └── lib/                    # API client, TypeScript types, utilities
│
├── .env.example
├── Makefile
└── pyproject.toml
```

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- [Anthropic API key](https://console.anthropic.com)
- [Google Places API key](https://developers.google.com/maps/documentation/places/web-service/get-api-key) with the following APIs enabled:
  - Places API (Nearby Search, Text Search, Place Details)
  - Geocoding API

---

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/your-username/market-research-agent.git
cd market-research-agent
```

**2. Install dependencies**

```bash
make install
```

This installs the Python package (`pip install -e backend/`) and the Node packages (`npm install --prefix frontend`).

**3. Configure environment variables**

```bash
cp .env.example .env
```

Then edit `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_PLACES_API_KEY=AIza...
CLAUDE_MODEL=claude-sonnet-4-6
MAX_TOKENS=16000
LOG_LEVEL=INFO
NEXT_PUBLIC_API_URL=http://localhost:8001
```

**4. Start development servers**

```bash
make dev
```

This starts both servers concurrently:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API docs (Swagger): http://localhost:8001/docs

---

## Running Servers Separately

```bash
# Terminal 1 — Backend
make backend
# or: uvicorn app.main:app --reload --port 8001 --app-dir backend

# Terminal 2 — Frontend
make frontend
# or: npm run dev --prefix frontend
```

---

## API Reference

### `POST /research`

**Request body:**

```json
{
  "address": "Shoreditch High Street, London, UK",
  "business_type": "cafe",
  "radius_meters": 1000,
  "max_competitors": 20
}
```

**Response:**

```json
{
  "request_address": "Shoreditch High Street, London, UK",
  "request_business_type": "cafe",
  "executive_summary": "...",
  "competitors": [
    {
      "name": "Workshop Coffee",
      "address": "60 Holborn Viaduct, London",
      "rating": 4.5,
      "user_ratings_total": 312,
      "price_level": 2,
      "distance_meters": 420,
      "competitive_score": 78
    }
  ],
  "location_score": {
    "overall": 64,
    "competition_density": 45,
    "accessibility_proxy": 82,
    "demand_signal": 71,
    "notes": ["High foot traffic area", "Saturated specialty coffee market"]
  },
  "traffic_estimate": {
    "busy_hours_summary": "Peak 8–10 AM and 12–2 PM on weekdays",
    "peak_day": "Saturday",
    "estimated_daily_footfall": "high",
    "confidence": "medium",
    "reasoning": "..."
  },
  "market_gaps": [
    {
      "gap_type": "Specialty roastery",
      "description": "No on-site roasting or single-origin focus within 1km",
      "opportunity_score": 72,
      "supporting_evidence": ["..."]
    }
  ],
  "recommendations": ["..."]
}
```

### `GET /health`

Returns `{"status": "ok"}` — used for health checks.

---

## Architecture

```
Frontend (Next.js :3000)
        │
        │ POST /research
        ▼
Backend (FastAPI :8001)
        │
        ▼
  ResearchService
        │
        ▼
  OrchestratorAgent  ──── geocode_address ────► Google Geocoding API
        │
        │  asyncio.gather()
        ├────────────────────────────────────────┐
        ▼                                        ▼
  CompetitorAgent                          LocationAgent
  TrafficAgent                             GapAgent
        │                                        │
        └──────────── Claude (tool-calling) ─────┘
                              │
                    Google Places API
                    (nearby_search, text_search, place_details)
                              │
                    JSON outputs from all 4 agents
                              │
                    OrchestratorAgent synthesizes
                              │
                    MarketResearchReport (Pydantic)
                              │
                    ResearchResponse → Frontend
```

Each agent runs a tool-calling loop: Claude emits a tool call → the backend executes it against Google Places → the result is fed back into the message history → repeat until `stop_reason == "end_turn"`. The orchestrator then synthesizes all four JSON outputs into one final report.

---

## Agent Design Patterns

- **Agentic loop** — each sub-agent iterates until Claude signals completion, not a fixed number of turns
- **Parallel execution** — all four sub-agents run simultaneously with `asyncio.gather()`
- **JSON-only output** — system prompts enforce structured JSON responses for reliable parsing
- **Tool dispatch** — `tools/registry.py` maps tool names to implementations, keeping agent logic clean
- **Stateless pipeline** — no database; each request spins up fresh agent instances

---

## Deployment

The project does not include Docker configuration. Below are minimal starting points.

**Backend:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend /app
RUN pip install -e .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Frontend:**

Deploy the `frontend/` directory to Vercel, AWS Amplify, or any Node.js host. Set `NEXT_PUBLIC_API_URL` to your backend URL.

**CORS:** Update `allow_origins` in `backend/app/main.py` to include your production frontend domain.

---

## License

MIT
