"""TerraSeek FastAPI application entry point."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from terraseek.routes import router
from terraseek.storage import init_storage

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

app = FastAPI(
    title="TerraSeek",
    description="Evidence-backed Earth observation investigation engine",
    version="0.2.0",
)

init_storage()

# API routes
app.include_router(router, prefix="/api/v1")

# Local evidence assets are served read-only so the offline demo can replay
# the same Sentinel-2 probe used by the backend and exported packages.
if DATA_DIR.is_dir():
    app.mount("/data", StaticFiles(directory=str(DATA_DIR)), name="data")

# Serve frontend static files
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
