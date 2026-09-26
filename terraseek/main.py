"""TerraSeek FastAPI application entry point."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from terraseek.routes import router

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(
    title="TerraSeek",
    description="Evidence-backed Earth observation investigation engine",
    version="0.1.0",
)

# API routes
app.include_router(router, prefix="/api/v1")

# Serve frontend static files
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
