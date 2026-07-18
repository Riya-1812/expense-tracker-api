from flask import Blueprint, request, jsonify, abort
from . import get_db

bp = Blueprint("expenses", __name__, url_prefix="/api")


def row_to_dict(row):
    return {
        "id": row["id"],
        "description": row["description"],
        "amount": row["amount"],
        "category": row["category"],
        "created_at": row["created_at"],
    }


@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@bp.route("/expenses", methods=["POST"])
def create_expense():
    data = request.get_json(silent=True) or {}
    description = data.get("description")
    amount = data.get("amount")
    category = data.get("category")

    if not description or amount is None or not category:
        abort(400, description="description, amount, and category are required")
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        abort(400, description="amount must be a number")

    db = get_db()
    cur = db.execute(
        "INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)",
        (description, amount, category),
    )
    db.commit()
    new_row = db.execute("SELECT * FROM expenses WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(new_row)), 201


@bp.route("/expenses", methods=["GET"])
def list_expenses():
    category = request.args.get("category")
    db = get_db()
    if category:
        rows = db.execute("SELECT * FROM expenses WHERE category = ? ORDER BY id DESC", (category,)).fetchall()
    else:
        rows = db.execute("SELECT * FROM expenses ORDER BY id DESC").fetchall()
    return jsonify([row_to_dict(r) for r in rows])


@bp.route("/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    db = get_db()
    row = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    if row is None:
        abort(404, description="expense not found")
    return jsonify(row_to_dict(row))


@bp.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    db = get_db()
    row = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    if row is None:
        abort(404, description="expense not found")

    data = request.get_json(silent=True) or {}
    description = data.get("description", row["description"])
    amount = data.get("amount", row["amount"])
    category = data.get("category", row["category"])
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        abort(400, description="amount must be a number")

    db.execute(
        "UPDATE expenses SET description = ?, amount = ?, category = ? WHERE id = ?",
        (description, amount, category, expense_id),
    )
    db.commit()
    updated = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    return jsonify(row_to_dict(updated))


@bp.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    db = get_db()
    row = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    if row is None:
        abort(404, description="expense not found")
    db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    db.commit()
    return "", 204


@bp.route("/summary", methods=["GET"])
def summary():
    db = get_db()
    rows = db.execute(
        "SELECT category, SUM(amount) as total, COUNT(*) as count FROM expenses GROUP BY category ORDER BY total DESC"
    ).fetchall()
    return jsonify([{"category": r["category"], "total": r["total"], "count": r["count"]} for r in rows])


@bp.errorhandler(400)
@bp.errorhandler(404)
def handle_error(e):
    return jsonify({"error": e.description}), e.code
