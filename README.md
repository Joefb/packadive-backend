# Packadive Backend (Flask API)

> Backend API for **Packadive** — a dive-trip packing and checklist application.

**Live API (Render):** <https://api.packadive.com>
**Live Frontend (Vercel):** <https://packadive.vercel.app/>
**Frontend Repo:** <https://github.com/Joefb/packadive>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [API Base URL](#api-base-url)
- [Authentication (JWT)](#authentication-jwt)
- [Main Routes (High Level)](#main-routes-high-level)
- [Database Schema (High Level)](#database-schema-high-level)
- [Local Development](#local-development)
- [Local Test Database](#local-test-database)
- [Database Migrations](#database-migrations)
- [CORS](#cors)
- [End-to-End Run (Frontend + Backend)](#end-to-end-run-frontend--backend)
- [Production](#production)
- [Project Structure](#project-structure)
- [Security Notes](#security-notes)
- [License](#license)
- [Contact](#contact)

---

## Overview

Packadive Backend is a **Flask REST API** that powers authentication and checklist functionality for the Packadive frontend. It supports user accounts, checklist CRUD, list item status tracking, and includes production-minded features like rate limiting and caching.

---

## Features

- **User Management**: registration, authentication, and profile management
- **Checklist Management**: create, read, update, delete checklists
- **List Items**: manage items within a checklist, including status tracking
- **JWT Authentication**: signed tokens
- **Rate Limiting**: API rate limiting to prevent abuse
- **Caching**: response caching for improved performance
- **CORS Enabled**: allows the deployed Vercel frontend to call this API
- **API Documentation**: Swagger/OpenAPI support (configurable)

---

## Tech Stack

- **Framework:** Flask 3.1.2
- **ORM:** SQLAlchemy 2.0.44 + Flask-SQLAlchemy 3.1.1
- **Serialization:** Marshmallow 4.1.0 + flask-marshmallow 1.3.0
- **Database:** PostgreSQL (production), SQLite (development/testing)
- **Auth:** python-jose 3.5.0 (JWT)
- **Rate Limiting:** Flask-Limiter 4.0.0
- **Caching:** Flask-Caching 2.3.1
- **Server:** Gunicorn 23.0.0

---

## API Base URL

- Production: `https://packadive-backend.onrender.com`
- Local (default Flask): `http://127.0.0.1:5000`

---

## Authentication (JWT)

Protected endpoints expect a header like:

```http
Authorization: Bearer <your_token_here>
```

Tokens are signed and verified using `SECRET_KEY`.

---

## Main Routes (High Level)

Base paths (registered as Flask blueprints):

- `/user` — registration, login, profile management
- `/checklists` — checklist CRUD and user checklist listing
- `/list_item` — checklist item CRUD + status updates

---

## Database Schema (High Level)

### User

- `id` (PK)
- `user_name` (unique)
- `password` (hashed)
- `email` (unique)
- Relationship: one user → many checklists

### CheckList

- `id` (PK)
- `checklist_name`
- `user_id` (FK → User)
- Relationship: one checklist → many list items

### ListItems

- `id` (PK)
- `item_name`
- `status`
- `checklist_id` (FK → CheckList)

---

## Local Development

### Prerequisites

- Python 3.8+
- (Optional) Podman, if you want to run against Postgres locally via `scripts/test-db.sh`

### Setup

```bash
git clone https://github.com/Joefb/packadive-backend.git
cd packadive-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration / Environment Variables

#### Required

- `SECRET_KEY` — used to sign and verify JWT tokens

#### Database

This project supports SQLite by default for development, and Postgres in production (and, optionally, for local development too — see [Local Test Database](#local-test-database)).

**Important note about variable names:**

- Some docs refer to `DATABASE_URL`
- The current `config.py` uses `SQLALCHEMY_DATABASE_URI` (especially in `ProductionConfig` and `DevelopmentConfig`)

Recommended dev env:

```bash
export SECRET_KEY=dev-secret
export FLASK_APP=wsgi.py
# optional — omit to fall back to sqlite:///app.db
export SQLALCHEMY_DATABASE_URI=sqlite:///app.db
```

Run:

```bash
flask run
```

`FLASK_CONFIG` selects which config class from `config.py` to load and defaults to `DevelopmentConfig` (set `FLASK_CONFIG=ProductionConfig`, etc. to override).

---

## Local Test Database

For dev/testing against the same database engine as production, spin up an isolated local Postgres container (separate from prod — its own container name, port, and no shared network):

```bash
./scripts/test-db.sh up      # start
./scripts/test-db.sh down    # stop and remove
./scripts/test-db.sh reset   # recreate from scratch
```

Defaults to `postgresql://packadive:packadive@localhost:5433/packadive_test` (override via `TEST_DB_PORT` / `TEST_DB_NAME` / `TEST_DB_USER` / `TEST_DB_PASSWORD`). Point `SQLALCHEMY_DATABASE_URI` at it:

```bash
export SQLALCHEMY_DATABASE_URI=postgresql://packadive:packadive@localhost:5433/packadive_test
flask db upgrade   # apply migrations
flask run
```

---

## Database Migrations

Schema changes are tracked with Flask-Migrate (Alembic) — `flask db upgrade` applies pending migrations, `flask db migrate -m "..."` autogenerates a new one from model changes (diff it against an empty database, e.g. the local test container above, so the generated migration reflects the real change rather than a no-op against an already-up-to-date dev DB). `entrypoint.sh` runs `flask db upgrade` automatically before starting Gunicorn in production.

---

## CORS

CORS is enabled in the Flask app (via `flask_cors.CORS(app)`), allowing the Vercel frontend to call the API.

If you ever want to restrict origins (more secure), configure CORS to only allow:

- `https://packadive.vercel.app`

---

## End-to-End Run (Frontend + Backend)

### Option A — Use deployed backend (fastest)

- API: <https://packadive-backend.onrender.com>
- Start frontend locally:

```bash
git clone https://github.com/Joefb/packadive.git
cd packadive
npm install
npm run dev
```

Then:

- Sign up / log in
- Create checklist → add items → toggle status
- Use Dive Conditions page for weather/forecast

### Option B — Run everything locally

1) Start backend:

```bash
flask run
```

1) Start frontend:

```bash
npm run dev
```

1) Confirm:

- Auth works (JWT)
- CRUD works for checklists/items
- Status updates persist

---

## Production

## Production

[#production](#production)

The API runs in a Podman container on a self-hosted server, with Postgres running in a separate rootless Podman container on the same private network. Public access is provided via a Cloudflare Tunnel — no inbound ports are opened on the host.

### Container build

The image is built from the included `Dockerfile`:

```bash
podman build -t packadive-backend:latest .
```

`entrypoint.sh` runs `flask db upgrade` once on container start to apply any pending migrations, then hands off to Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('ProductionConfig')"
```

> Note: the prod database was originally created via SQLAlchemy's `db.create_all()`, before Flask-Migrate was introduced. The first time this migrations-based `entrypoint.sh` ships to prod, the prod DB must be stamped with the baseline migration (`flask db stamp head` against the prod `SQLALCHEMY_DATABASE_URI`, run manually) *before* the deploy — otherwise `flask db upgrade` will try to create tables that already exist and the container will fail to start.

### Auto-deploy

`deploy.sh` polls `origin/main` on a 5-minute systemd timer. When new commits are detected, it pulls, rebuilds the image, and restarts the API container via `systemctl --user restart`.

**Note:** `deploy.sh` currently hardcodes the repo's absolute path (`/home/joefb/services/packadive-backend`). If this deployment is ever moved to a different host or path, update `REPO_DIR` in `deploy.sh` accordingly
---

## Project Structure

```text
packadive-backend/
├── app/
│   ├── __init__.py          # Flask app factory + blueprint registration + CORS
│   ├── models.py            # SQLAlchemy models
│   ├── extensions.py        # Marshmallow, Limiter, Cache initialization
│   ├── blueprints/          # API route blueprints
│   │   ├── user/
│   │   ├── checklist/
│   │   └── list_item/
│   ├── util/                # auth utilities, helpers
│   └── static/              # Swagger specs, etc. (optional)
├── instance/
├── migrations/               # Flask-Migrate / Alembic migrations
├── scripts/
│   └── test-db.sh            # local test Postgres container (up/down/reset)
├── config.py
├── wsgi.py                   # FLASK_APP entrypoint (flask run / flask db ...)
├── requirements.txt
└── README.md
```

---

## Security Notes

[#security-notes](#security-notes)

- Use a strong `SECRET_KEY` in production.
- Prefer HTTPS (provided via Cloudflare Tunnel in production).
- Rate limiting is enabled — tune limits as needed.
- Avoid hard-coded credentials if you ever re-enable "default admin" logic.
- API responses use `user_return_schema`, which excludes the password hash. Always use this schema (not `user_schema`) for any endpoint returning user data.

---

## License

MIT License © 2026 Joefb

---

## Contact

Project Owner: [Joefb](https://github.com/Joefb)  
Project Link: <https://github.com/Joefb/packadive-backend>
Auto-deploy test Thu Jul 16 04:43:50 PM PDT 2026
