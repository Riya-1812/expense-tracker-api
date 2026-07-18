# Expense Tracker REST API

A small REST API for tracking personal expenses, built with Flask and SQLite.
Demonstrates CRUD design, request validation, and a simple aggregation endpoint.

## Features
- `POST /api/expenses` — create an expense
- `GET /api/expenses` — list expenses (optional `?category=` filter)
- `GET /api/expenses/<id>` — get one expense
- `PUT /api/expenses/<id>` — update an expense
- `DELETE /api/expenses/<id>` — delete an expense
- `GET /api/summary` — total spend and count grouped by category
- `GET /api/health` — health check

## Run locally
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
Server runs at `http://localhost:5000`.

## Try it
```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{"description": "Groceries", "amount": 42.50, "category": "food"}'

curl http://localhost:5000/api/expenses
curl http://localhost:5000/api/summary
```

## Deploying
This runs anywhere Python does:
- **Render / Railway**: connect the repo, set start command to `gunicorn run:app`.
- **Docker**: add a `Dockerfile` with `FROM python:3.12-slim`, copy the app, `pip install -r requirements.txt`, `CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]`.

## Possible extensions (good talking points in interviews)
- Swap SQLite for PostgreSQL using SQLAlchemy for a production-grade setup.
- Add user accounts + auth (JWT) so expenses are per-user.
- Add pagination to `GET /api/expenses`.
- Add automated tests with `pytest` + Flask's test client.
