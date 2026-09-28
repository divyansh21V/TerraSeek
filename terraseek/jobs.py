"""Lightweight background jobs for the hackathon deployment."""

from __future__ import annotations

import threading
import uuid
from collections.abc import Callable

_jobs: dict[str, dict] = {}


def submit(work: Callable[[], dict]) -> str:
    job_id = f"job-{uuid.uuid4().hex[:12]}"
    _jobs[job_id] = {"id": job_id, "status": "queued", "result": None, "error": None}

    def run() -> None:
        _jobs[job_id]["status"] = "running"
        try:
            _jobs[job_id]["result"] = work()
            _jobs[job_id]["status"] = "completed"
        except Exception as exc:  # noqa: BLE001  # job failures must be reported to callers
            _jobs[job_id]["error"] = str(exc)
            _jobs[job_id]["status"] = "failed"

    threading.Thread(target=run, name=f"terraseek-{job_id}", daemon=True).start()
    return job_id


def get(job_id: str) -> dict | None:
    return _jobs.get(job_id)
