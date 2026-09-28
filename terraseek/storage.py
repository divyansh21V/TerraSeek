"""Small SQLite persistence layer for local and hackathon deployments."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any


def _db_path() -> Path:
    return Path(os.getenv("TERRASEEK_DB_PATH", "terraseek.db"))


def _connect() -> sqlite3.Connection:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def init_storage() -> None:
    """Create the local persistence schema if it does not exist."""
    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS investigations (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS decisions (
                investigation_id TEXT NOT NULL,
                candidate_id TEXT NOT NULL,
                payload TEXT NOT NULL,
                recorded_at TEXT NOT NULL,
                PRIMARY KEY (investigation_id, candidate_id)
            );
            """
        )


def save_investigation(investigation_id: str, payload: dict[str, Any], created_at: str) -> None:
    with _connect() as connection:
        connection.execute(
            "INSERT OR REPLACE INTO investigations(id, payload, created_at) VALUES (?, ?, ?)",
            (investigation_id, json.dumps(payload), created_at),
        )


def load_investigation(investigation_id: str) -> dict[str, Any] | None:
    with _connect() as connection:
        row = connection.execute(
            "SELECT payload FROM investigations WHERE id = ?", (investigation_id,)
        ).fetchone()
    return json.loads(row["payload"]) if row else None


def save_decision(
    investigation_id: str, candidate_id: str, payload: dict[str, Any], recorded_at: str
) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO decisions(investigation_id, candidate_id, payload, recorded_at)
            VALUES (?, ?, ?, ?)
            """,
            (investigation_id, candidate_id, json.dumps(payload), recorded_at),
        )


def load_decisions(investigation_id: str) -> dict[str, dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT candidate_id, payload FROM decisions WHERE investigation_id = ?",
            (investigation_id,),
        ).fetchall()
    return {row["candidate_id"]: json.loads(row["payload"]) for row in rows}
