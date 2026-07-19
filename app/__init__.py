import os
import sqlite3
from flask import Flask, g

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "expenses.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        conn = sqlite3.connect(DB_PATH)
        conn.executescript(SCHEMA)
        conn.commit()
        conn.close()


HOMEPAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Expense Tracker API</title>
<style>
  body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; background: #f5f3f8; color: #2d2438; margin: 0; padding: 60px 20px; }
  .card { max-width: 640px; margin: 0 auto; background: white; border-radius: 12px; padding: 40px; box-shadow: 0 4px 20px rgba(107,78,142,0.12); }
  h1 { color: #6b4e8e; margin-top: 0; }
  p.lead { color: #555; }
  code { background: #f0ecf6; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
  table { width: 100%; border-collapse: collapse; margin-top: 24px; }
  th, td { text-align: left; padding: 10px 8px; border-bottom: 1px solid #eee; font-size: 0.92em; }
  th { color: #6b4e8e; }
  .method { font-weight: 600; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }
  .get { background: #e6f4ea; color: #1e7a34; }
  .post { background: #e7f0fd; color: #1a56b0; }
  .put { background: #fff3d9; color: #93600b; }
  .delete { background: #fde8e8; color: #b0221a; }
  a { color: #6b4e8e; }
  footer { margin-top: 28px; font-size: 0.85em; color: #888; }
</style>
</head>
<body>
  <div class="card">
    <h1>&#128184; Expense Tracker API</h1>
    <p class="lead">A small REST API for tracking personal expenses, built with Flask and SQLite.</p>
    <p>Try it now: <a href="/api/expenses">/api/expenses</a> &middot; <a href="/api/summary">/api/summary</a> &middot; <a href="/api/health">/api/health</a></p>
    <table>
      <tr><th>Method</th><th>Endpoint</th><th>What it does</th></tr>
      <tr><td><span class="method post">POST</span></td><td><code>/api/expenses</code></td><td>Create an expense</td></tr>
      <tr><td><span class="method get">GET</span></td><td><code>/api/expenses</code></td><td>List all expenses</td></tr>
      <tr><td><span class="method get">GET</span></td><td><code>/api/expenses/&lt;id&gt;</code></td><td>Get one expense</td></tr>
      <tr><td><span class="method put">PUT</span></td><td><code>/api/expenses/&lt;id&gt;</code></td><td>Update an expense</td></tr>
      <tr><td><span class="method delete">DELETE</span></td><td><code>/api/expenses/&lt;id&gt;</code></td><td>Delete an expense</td></tr>
      <tr><td><span class="method get">GET</span></td><td><code>/api/summary</code></td><td>Totals by category</td></tr>
    </table>
    <footer>Built by Riya Thakur &middot; <a href="https://github.com/Riya-1812/expense-tracker-api">View source on GitHub</a></footer>
  </div>
</body>
</html>
"""


def create_app():
    app = Flask(__name__)
    app.teardown_appcontext(close_db)
    init_db(app)

    from . import routes
    app.register_blueprint(routes.bp)

    @app.route("/")
    def homepage():
        return HOMEPAGE_HTML

    return app
