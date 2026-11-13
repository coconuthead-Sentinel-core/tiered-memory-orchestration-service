import asyncio
import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router
from .infrastructure.cosmos_repo import CosmosDBRepository
from .runtime_ai import ai_runtime
from .services.cno_ax_engine import cno_ax_engine
from .services.uismt import uismt
from .ws_api import router as ws_router

# Set event loop policy for Windows
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentinel-middleware")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Cosmos DB Repository (will use Mock DB mode if unavailable)
    await CosmosDBRepository.initialize()
    logger.info("Cosmos DB Repository initialized.")

    ai_status = await ai_runtime.probe()
    if ai_status["verified_live_access"]:
        logger.info("AI runtime probe successful: %s", ai_status["selected_provider"])
    else:
        logger.warning(
            "AI runtime is not verified for live scoring: %s", ai_status["auth_detail"]
        )

    # Auto-start 1000 Strikes Simulation
    logger.info("🚀 Auto-starting 1000 Strikes Protocol...")
    uismt.thread_input("START 1000 STRIKES", input_type="command")
    asyncio.create_task(cno_ax_engine.start_traffic_optimization_loop())

    yield

    # Cleanup on shutdown
    await CosmosDBRepository.close()
    await ai_runtime.aclose()


app = FastAPI(title="Neurodivergent AI Middleware", lifespan=lifespan)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NOTE: Old middleware for request size, rate limiting, and API key are removed.
# New implementation uses dependency injection (`api_key_guard`) and Pydantic settings.

# Include routers
app.include_router(api_router, prefix="/api")
app.include_router(ws_router)
# app.include_router(ai_router, prefix="/api")


@app.post("/api/testpost")
async def test_post():
    return {"message": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=75, log_level="info")
