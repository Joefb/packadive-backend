# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Packadive Backend is a Flask REST API powering auth and checklist functionality for the Packadive dive-trip packing app. Flask 3.1 + SQLAlchemy 2.0 (`Mapped`/`mapped_column` style) + Marshmallow 4 for serialization, JWT auth via `python-jose`, PostgreSQL in production / SQLite in dev.

## Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Required env vars for local dev
export SECRET_KEY=dev-secret
export FLASK_APP=wsgi.py
export SQLALCHEMY_DATABASE_URI=sqlite:///app.db   # optional, defaults to sqlite:///app.db

# Run dev server
flask run

# Local Postgres for dev/testing (isolated from prod — own container/port/network)
./scripts/test-db.sh up      # / down / reset
flask db upgrade              # apply migrations to whichever SQLALCHEMY_DATABASE_URI is set

# Or run the actual prod image (Dockerfile/entrypoint.sh) against the test DB
./scripts/test-app.sh build  # / up / down / logs
```

`FLASK_CONFIG` selects the `config.py` class to load (defaults to `DevelopmentConfig`); `wsgi.py` is the single `FLASK_APP` entrypoint used by both `flask run` and `flask db ...`.

There is no test suite, linter, or formatter configured in this repo (no `pytest`, `flake8`, `ruff`, `black`, etc. in `requirements.txt`, no test files present).

### Production / Docker

```bash
podman build -t packadive-backend:latest .
```

`entrypoint.sh` runs `flask db upgrade` (against `ProductionConfig`) once, then execs:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('ProductionConfig')"
```

Deployed as a rootless Podman container behind a Cloudflare Tunnel (no open inbound ports). `deploy.sh` runs on a systemd timer, polls `origin/main`, and rebuilds/restarts the container on new commits — it hardcodes `REPO_DIR=/home/joefb/services/packadive-backend`.

## Architecture

**App factory + blueprints.** `app/__init__.py` exposes `create_app(config_name)`, which loads a class from `config.py` (`DevelopmentConfig` / `TestingConfig` / `ProductionConfig`), initializes the shared extension singletons from `app/extensions.py` (`db`, `ma`, `limiter`, `cache`, `migrate`), applies CORS, and registers three blueprints under fixed prefixes:

- `/user` — `app/blueprints/user`
- `/checklists` — `app/blueprints/checklist`
- `/list_item` — `app/blueprints/list_item`

Each blueprint package follows the same shape: `__init__.py` creates the `Blueprint` object and imports `routes` at the bottom (avoids circular imports), `routes.py` holds view functions, `schemas.py` holds the Marshmallow schemas for that resource.

**Models** (`app/models.py`): `User` → `CheckList` (one-to-many) → `ListItems` (one-to-many), using SQLAlchemy 2.0 declarative `Mapped[...]` typing. Schema changes go through Flask-Migrate (`migrations/`) — the prod DB was originally built via `db.create_all()` and stamped with the baseline migration afterward, so `flask db migrate` is now the source of truth going forward. Autogenerate new migrations by diffing against an empty database (e.g. `scripts/test-db.sh up`), not an already-up-to-date dev DB, or the diff will come back empty.

**Auth** (`app/util/auth.py`): custom JWT via `python-jose`, not Flask extensions. `encode_auth_token` signs `{sub, user_name, iat, exp}`. Two decorators gate routes: `auth_token_required` (any valid token, sets `request.logged_in_id`) and `admin_auth_token_required` (additionally requires `user_name == "admin"` in the token payload — there's no `is_admin` DB flag, admin-ness is purely encoded in the JWT). The signing key comes from `os.environ.get("SECRET_KEY")` read directly in `auth.py`, independent of Flask's `app.config` — `config.py` also defines a module-level `SECRET_KEY` but none of the `*Config` classes set it as a class attribute, so it is never actually loaded into `app.config`. Set `SECRET_KEY` in the environment; don't expect changing `config.py` to affect token signing.

**Schemas / data loading inconsistency**: `ListItemsSchema` sets `load_instance = True`, so `.load()` returns a `ListItems` model instance (attribute access, e.g. `data.item_name` in `list_item/routes.py`). `UserSchema` and `CheckListSchema` do not set `load_instance`, so their `.load()` returns a plain dict (`data["user_name"]`). Check which pattern a given schema uses before consuming its `.load()` output.

**User responses must exclude the password hash.** Always serialize outgoing user data with `user_return_schema` (`exclude=("password",)`), never the base `user_schema` or `create_user_schema`, which include the raw password field.

**Rate limiting** is per-route via `@limiter.limit(...)` decorators (Flask-Limiter, in-memory storage, default global limits `2000/day, 500/hour` set in `app/extensions.py`). Follow the existing convention of tighter limits on write/auth endpoints (e.g. login is `5 per minute`, user creation `3 per hour`) when adding new routes.

**CORS** is scoped in `app/__init__.py` to `https://www.packadive.com` and `https://packadive.com` only, overridable via the `CORS_ORIGINS` env var (comma-separated) for local testing against a frontend dev server — leave it unset in prod so the hardcoded list stays in force. Update the hardcoded list, not a blanket `CORS(app)`, if a new frontend origin needs *permanent* access.

**Ownership checks**: checklist and list-item routes always scope queries by the authenticated user (`request.logged_in_id`), either directly (`filter_by(user_id=...)` for checklists) or by walking `ListItems.checklist_id → CheckList.user_id` (for list items, since `ListItems` has no direct `user_id`). Preserve this pattern for any new item/checklist routes to avoid IDOR-style access.
