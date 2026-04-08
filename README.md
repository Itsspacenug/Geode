# Forge

A smart schedule optimizer for Colorado School of Mines students. Forge takes your required courses and personal preferences, generates every valid schedule, and surfaces the best options so you can spend less time wrestling with registration and more time on what matters.

---

## What It Does

University registration is stressful. Sections conflict, the good time slots fill fast, and building the "perfect" schedule by hand is tedious. Forge automates that process.

You tell Forge:
- Which courses you need to take
- What your schedule should *feel* like (compact, spacey, grouped by day, spread out, etc.)

Forge handles the rest, finding every conflict-free schedule and ranking them by how well they match your preferences.

---

## Features

- **Schedule Optimizer** — generates all valid, conflict-free schedules from your selected courses and sections
- **Preference-Based Scoring** — rank schedules by compactness, day grouping, breathing room, subject adjacency, and more
- **"Best Effort" Mode** — always returns the best available option even when ideal constraints cannot be fully met
- **Course Watchlist** — monitor seat availability and waitlist status for sections you care about
- **Notifications** — get alerted via email, SMS, or in-app when a watched section opens up
- **Dashboard** — view your saved schedules, watchlisted sections, and upcoming registration windows

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, React Query |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy + Alembic |
| Background Jobs | APScheduler |
| Notifications | SendGrid (email), Twilio (SMS) |
| Auth | JWT (access + refresh tokens) |
| Deployment | Vercel (frontend), Render/Railway (backend) |

---

## Project Structure

```
forge/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI route handlers
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── optimizer/      # Schedule generation + scoring engine
│   │   ├── scraper/        # Mines catalog integration
│   │   ├── notifications/  # Email, SMS, in-app dispatch
│   │   └── core/           # Config, auth, database setup
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── api/            # React Query API calls
│   └── package.json
├── models.py               # Core data models (TimeBlock, Section, Course)
├── scheduler.py            # Conflict detection logic
├── web_scraper.py          # Mines catalog scraper
├── mines_catalog.json      # Scraped course data
└── README.md
```

---

## Core Modules

### `models.py`

Defines the three foundational dataclasses the optimizer operates on.

- **`TimeBlock`** represents a single time slot with a `day` (integer, 0 = Monday), `start`, and `end` (both in minutes from midnight). Includes an `overlaps_with` method that checks same-day intersection.
- **`Section`** represents one section of a course: a CRN, section ID, course code, department, and a list of `TimeBlock` objects.
- **`Course`** groups sections together under a course name, code, and department.

### `scheduler.py`

Contains `section_conflicts_with_schedule(section, schedule)`, which takes a candidate `Section` and a list of already-placed `Section` objects and returns `True` if any time blocks overlap. This is the hard-constraint check at the heart of the optimizer.

### `web_scraper.py`

Scrapes the Mines course catalog at `catalog.mines.edu` using `requests` and `BeautifulSoup`. It walks every department URL, extracts course blocks, and parses out course codes, prerequisites, and corequisites via regex. Output is written to `mines_catalog.json`. A 1-second delay between requests keeps it polite to Mines servers.

### `mines_catalog.json`

The scraped course catalog. Each entry is a JSON object with `code`, `name`, `prereqs`, and `coreqs`. This file seeds course data for the POC without requiring a live database connection.

---

## The Optimizer

The core of Forge is a **constraint satisfaction + scoring engine**.

1. **Generate** — uses backtracking to build all conflict-free schedule combinations, pruning invalid branches early via `section_conflicts_with_schedule`
2. **Score** — each valid schedule is scored against the user's preferences (compactness, day balance, adjacency, etc.)
3. **Rank** — the top N schedules are returned, ordered by score

Time conflicts are **hard constraints** (they eliminate a schedule entirely). User preferences are **soft constraints** (they affect scoring but never disqualify a schedule). This means Forge always returns a result, the best it can do with what is available.

---

## Current Status

This is a proof-of-concept targeting Colorado School of Mines. The core data models and conflict-detection logic are implemented. The scraper has run successfully against the live Mines catalog and produced `mines_catalog.json`. The full scoring engine, API, and frontend are under active development.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env

alembic upgrade head

uvicorn app.main:app --reload
```

API available at `http://localhost:8000`. Auto-generated docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`.

### Running the Scraper

```bash
python web_scraper.py
```

Outputs `mines_catalog.json` in the project root.

---

## Roadmap

- [x] Core data models (`TimeBlock`, `Section`, `Course`)
- [x] Conflict detection (`section_conflicts_with_schedule`)
- [x] Mines catalog scraper + `mines_catalog.json`
- [ ] Schedule generation engine (backtracking)
- [ ] Preference scoring engine
- [ ] FastAPI backend + REST endpoints
- [ ] User auth (register, login, JWT)
- [ ] Course watchlist + seat monitoring
- [ ] Notification dispatch (email, SMS, in-app)
- [ ] React frontend + preference UI
- [ ] Multi-university support

---

## Contributing

This project is in early development. If you would like to contribute, open an issue first to discuss what you would like to change.