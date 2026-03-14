import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from api.routes import router as game_router
from api.schemas import HealthResponse
from api.websocket.routes import router as ws_router

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Tic Tac Toe Multiplayer API",
    description="A real-time multiplayer Noughts and Crosses game backend",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_router)
app.include_router(ws_router)


@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Returns the health status of the API",
)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse()


@app.get("/", response_class=FileResponse)
async def read_index() -> str:
    return "index.html"
