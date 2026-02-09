# DeutschGorilla

German vocabulary trainer with AI-assisted learning modes.

## Project structure

- `backend/` — FastAPI backend (SQLite + SQLAlchemy)
- `frontend/` — Angular 17 frontend

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Seed 100 test words:

```bash
cd backend
PYTHONPATH=. python scripts/seed_words.py
```

## Frontend

```bash
cd frontend
npm install
npm start
```
