# Packadive Backend (Flask API)

> Backend API for **Packadive** — a dive-trip packing and checklist application.

**Live API (Render):** <https://packadive-backend.onrender.com>  
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
- (Optional) PostgreSQL if you want to run against Postgres locally

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

This project supports SQLite by default for development, and Postgres in production.

**Important note about variable names:**

- Some docs refer to `DATABASE_URL`
- The current `config.py` uses `SQLALCHEMY_DATABASE_URI` (especially in `ProductionConfig`)

Recommended dev env:

```bash
export SECRET_KEY=dev-secret
export SQLALCHEMY_DATABASE_URI=sqlite:///app.db
```

Run:

```bash
python planadive.py
```

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
python planadive.py
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

Example Gunicorn command:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"
```

> Note: `planadive.py` currently creates the app with `ProductionConfig` and creates tables on startup. That’s fine for a capstone deployment; larger systems typically use migrations in CI/CD.

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
├── config.py
├── planadive.py
├── requirements.txt
└── README.md
```

---

## Security Notes

- Use a strong `SECRET_KEY` in production.
- Prefer HTTPS (Render provides HTTPS).
- Rate limiting is enabled — tune limits as needed.
- Avoid hard-coded credentials if you ever re-enable “default admin” logic.

---

## License

MIT License © 2026 Joefb

---

## Contact

Project Owner: [Joefb](https://github.com/Joefb)  
Project Link: <https://github.com/Joefb/packadive-backend>
