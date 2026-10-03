"""One-off, idempotent: apply hub/schema.sql, create the hub_writer / hub_reader roles, grant, and append their URLs
to .env (passwords are generated here and never printed). Needs the owner's DATABASE_URL.

    uv run python -m hub.setup            # schema + roles + grants (+ .env lines if missing)
    uv run python -m hub.setup --schema   # schema and grants only (after editing schema.sql)
"""
import argparse
import secrets
import sys
from urllib.parse import quote, urlsplit, urlunsplit

from psycopg import sql

from hub.db import ROOT, connect, url_for

RAW = ("events", "leaderboard", "team_snapshots", "offers", "state", "state_history", "cards", "me_snapshots",
       "heartbeats", "gaps")
MODEL = ("model_runs", "team_mult", "team_card_value", "opportunities", "evidence")
ROLES = {"hub_writer": "HUB_WRITER_URL", "hub_reader": "HUB_READER_URL"}


def role_url(owner_url: str, role: str, password: str) -> str:
    u = urlsplit(owner_url)
    host = u.netloc.split("@", 1)[1]
    return urlunsplit((u.scheme, f"{role}:{quote(password, safe='')}@{host}", u.path, u.query, u.fragment))


def apply_schema(cur):
    cur.execute((ROOT / "hub" / "schema.sql").read_text())


def grant(cur):
    cur.execute("grant usage on schema hub to hub_writer, hub_reader")
    for t in RAW:
        cur.execute(sql.SQL("grant select, insert, update on hub.{} to hub_writer").format(sql.Identifier(t)))
    for t in MODEL:
        cur.execute(sql.SQL("grant select, insert, update, delete on hub.{} to hub_writer").format(sql.Identifier(t)))
    cur.execute("grant usage, select on all sequences in schema hub to hub_writer")
    cur.execute("grant select on all tables in schema hub to hub_reader, hub_writer")
    cur.execute("alter default privileges in schema hub grant select on tables to hub_reader, hub_writer")


def ensure_roles(cur, env_text: str, rotate: bool) -> dict:
    """Create missing roles with fresh passwords; return {ENV_NAME: url} for the URLs to append to .env.
    An existing role whose URL this .env lacks is left alone unless `rotate` (rotating breaks every other machine)."""
    owner = url_for("owner")
    new = {}
    for role, env in ROLES.items():
        cur.execute("select 1 from pg_roles where rolname = %s", (role,))
        exists = cur.fetchone() is not None
        has_env = any(line.strip().removeprefix("export ").startswith(env + "=") for line in env_text.splitlines())
        if exists and (has_env or not rotate):
            if not has_env:
                print(f"{role} exists but {env} is not in this .env: get it from Aleks (or --rotate on Aleks's machine)")
            continue
        pw = secrets.token_urlsafe(24)
        verb = "alter" if exists else "create"
        cur.execute(sql.SQL(verb + " role {} with login password {}").format(sql.Identifier(role), sql.Literal(pw)))
        new[env] = role_url(owner, role, pw)
    return new


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", action="store_true", help="schema and grants only")
    ap.add_argument("--rotate", action="store_true", help="reset the password of a role whose URL .env lacks")
    a = ap.parse_args(argv)
    env_path = ROOT / ".env"
    env_text = env_path.read_text() if env_path.exists() else ""
    with connect("owner") as c, c.cursor() as cur:
        apply_schema(cur)
        new = {} if a.schema else ensure_roles(cur, env_text, a.rotate)
        grant(cur)
    if new:
        with env_path.open("a") as f:
            f.write("\n# The hub (Neon): written by `python -m hub.setup`. Share privately, never commit.\n")
            for k, v in new.items():
                f.write(f'{k}="{v}"\n')   # quoted: the URL's "&" would break `source .env`
    print("schema applied; grants set;", f"new .env lines: {', '.join(new)}" if new else "roles and .env already set")


if __name__ == "__main__":
    sys.exit(main())
