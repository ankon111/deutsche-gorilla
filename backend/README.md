# DeutschGorilla Backend

FastAPI service implementing the DeutschGorilla API.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Seed test data

```bash
PYTHONPATH=. python scripts/seed_words.py
```

The seed script inserts 100 placeholder words with translations and examples.
