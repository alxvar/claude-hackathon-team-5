"""Connections to the hub (Neon Postgres). URLs come from .env and are never printed.

    HUB_WRITER_URL   collectors, importer, demand model (insert/update; deletes only in model tables)
    HUB_READER_URL   everyone else: dashboards, analysts, Claude sessions (read-only)
    DATABASE_URL     owner: schema changes and role setup only (`python -m hub.setup`)
"""
import os
import re
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

ROLE_ENV = {"writer": "HUB_WRITER_URL", "reader": "HUB_READER_URL", "owner": "DATABASE_URL"}


def url_for(role: str) -> str:
    name = ROLE_ENV[role]
    url = os.environ.get(name)
    if not url:
        raise SystemExit(f"{name} is not set (in .env): ask Aleks for the hub's {role} URL")
    return url


def connect(role: str = "reader", autocommit: bool = True) -> psycopg.Connection:
    return psycopg.connect(url_for(role), autocommit=autocommit, connect_timeout=15,
                           application_name=f"hub-{role}")


def redact(text: str) -> str:
    """Strip anything that looks like credentials from an error message before logging it."""
    return re.sub(r"(postgres(?:ql)?://)[^@\s]+@", r"\1***@", str(text))
