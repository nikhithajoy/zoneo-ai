from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes.research import router
from app.core.clients import close_http_client
from app.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Market Research Agent starting up...")
    yield
    logger.info("Shutting down — closing HTTP client...")
    await close_http_client()


app = FastAPI(
    title="Market Research Agent",
    description=(
        "Multi-agent pipeline for competitive market analysis. "
        "Combines Google Places API data with Claude AI to produce "
        "structured market research reports."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
