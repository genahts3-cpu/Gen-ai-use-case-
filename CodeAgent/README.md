# Gen AI Use Case Studio

A production-quality, hackathon-ready application for capturing, organizing, and showcasing GenAI use cases. The app ships with a FastAPI backend and a static single-page frontend.

## Features
- Create, update, delete, and search GenAI use cases
- Categorize and tag use cases
- Persist data to a JSON file for easy portability
- Simple single-page UI with real-time updates

## Tech Stack
- **Backend**: FastAPI
- **Frontend**: Vanilla HTML/CSS/JS
- **Persistence**: JSON file storage

## Quick Start

### 1) Create a virtual environment
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
```
pip install -r backend/requirements.txt
```

### 3) Run the server
```
uvicorn app.main:app --reload --app-dir backend
```

### 4) Open the app
Visit: http://127.0.0.1:8000

## API Overview
- `GET /api/usecases` — List all use cases
- `POST /api/usecases` — Create a new use case
- `PUT /api/usecases/{id}` — Update a use case
- `DELETE /api/usecases/{id}` — Delete a use case
- `GET /api/usecases/search?q=...` — Search use cases

## Data Storage
Data persists to `backend/app/data/usecases.json`. You can edit or seed this file manually.

## Notes
- This repository is self-contained and production-ready for hackathons.
- No external API keys required.
