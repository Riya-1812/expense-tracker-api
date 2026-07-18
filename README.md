# Expense Tracker REST API

A simple and practical REST API built with **Python, Flask, and SQLite** to manage personal expenses. This project demonstrates backend API development, CRUD operations, input validation, database handling, and building clean RESTful endpoints.

I built this project to practice designing a backend service that can create, manage, and analyze expense data through well-structured APIs.

## Features

* Create, view, update, and delete expenses
* Filter expenses by category
* Generate spending summaries grouped by category
* Health check endpoint for monitoring
* Request validation for safer API usage
* SQLite database integration

### Available Endpoints

| Method | Endpoint             | Description                                    |
| ------ | -------------------- | ---------------------------------------------- |
| POST   | `/api/expenses`      | Create a new expense                           |
| GET    | `/api/expenses`      | Get all expenses (supports category filtering) |
| GET    | `/api/expenses/<id>` | Get an expense by ID                           |
| PUT    | `/api/expenses/<id>` | Update an existing expense                     |
| DELETE | `/api/expenses/<id>` | Delete an expense                              |
| GET    | `/api/summary`       | View total spending and category-wise summary  |
| GET    | `/api/health`        | Check API health status                        |

## Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd expense-tracker-api
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python run.py
```

The API will be available at:

```
http://localhost:5001
```

## Example API Usage

Create an expense:

```bash
curl -X POST http://localhost:5000/api/expenses \
-H "Content-Type: application/json" \
-d '{"description":"Groceries","amount":42.50,"category":"food"}'
```

Get all expenses:

```bash
curl http://localhost:5001/api/expenses
```

Get expense summary:

```bash
curl http://localhost:5000/api/summary
```

## Project Structure

```
expense-tracker-api/
│
├── app/              # Flask application code
├── run.py            # Application entry point
├── requirements.txt  # Python dependencies
└── expenses.db       # SQLite database
```


## Deployment

The application can be deployed on platforms that support Python applications, such as Render or Railway.

For production deployment, it can be served using Gunicorn:

```bash
gunicorn run:app
```

## Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite
* **API Style:** REST
* **Tools:** Git, GitHub

---

Built as a backend engineering project to practice API design, database operations, and clean application structure.
