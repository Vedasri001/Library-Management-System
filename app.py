from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

# ─── In-memory data store ───────────────────────────────────────────────────

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "books": [
            {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic Fiction", "isbn": "978-0743273565", "total_copies": 3, "available_copies": 2, "added_date": "2024-01-10"},
            {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic Fiction", "isbn": "978-0061935466", "total_copies": 4, "available_copies": 4, "added_date": "2024-01-12"},
            {"id": 3, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "isbn": "978-0451524935", "total_copies": 5, "available_copies": 3, "added_date": "2024-01-15"},
            {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "isbn": "978-0141439518", "total_copies": 3, "available_copies": 1, "added_date": "2024-01-18"},
            {"id": 5, "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "isbn": "978-0547928227", "total_copies": 4, "available_copies": 4, "added_date": "2024-02-01"},
            {"id": 6, "title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "genre": "Fantasy", "isbn": "978-0439708180", "total_copies": 6, "available_copies": 2, "added_date": "2024-02-05"},
            {"id": 7, "title": "The Alchemist", "author": "Paulo Coelho", "genre": "Philosophy", "isbn": "978-0062315007", "total_copies": 3, "available_copies": 3, "added_date": "2024-02-10"},
            {"id": 8, "title": "Sapiens", "author": "Yuval Noah Harari", "genre": "Non-Fiction", "isbn": "978-0062316097", "total_copies": 4, "available_copies": 0, "added_date": "2024-02-15"},
        ],
        "users": [
            {"id": 1, "name": "Arjun Sharma", "email": "arjun.sharma@email.com", "phone": "9876543210", "member_type": "Student", "join_date": "2024-01-05", "status": "Active"},
            {"id": 2, "name": "Priya Reddy", "email": "priya.reddy@email.com", "phone": "9876543211", "member_type": "Faculty", "join_date": "2024-01-08", "status": "Active"},
            {"id": 3, "name": "Rahul Verma", "email": "rahul.verma@email.com", "phone": "9876543212", "member_type": "Student", "join_date": "2024-01-20", "status": "Active"},
            {"id": 4, "name": "Sneha Patel", "email": "sneha.patel@email.com", "phone": "9876543213", "member_type": "Student", "join_date": "2024-02-01", "status": "Active"},
            {"id": 5, "name": "Vikram Nair", "email": "vikram.nair@email.com", "phone": "9876543214", "member_type": "Staff", "join_date": "2024-02-10", "status": "Active"},
        ],
        "transactions": [
            {"id": 1, "book_id": 1, "user_id": 1, "issue_date": "2024-11-01", "due_date": "2024-11-15", "return_date": None, "status": "Issued", "fine": 0},
            {"id": 2, "book_id": 3, "user_id": 2, "issue_date": "2024-10-20", "due_date": "2024-11-03", "return_date": None, "status": "Issued", "fine": 0},
            {"id": 3, "book_id": 6, "user_id": 3, "issue_date": "2024-10-15", "due_date": "2024-10-29", "return_date": "2024-10-28", "status": "Returned", "fine": 0},
            {"id": 4, "book_id": 4, "user_id": 4, "issue_date": "2024-11-05", "due_date": "2024-11-19", "return_date": None, "status": "Issued", "fine": 0},
            {"id": 5, "book_id": 8, "user_id": 1, "issue_date": "2024-10-01", "due_date": "2024-10-15", "return_date": None, "status": "Overdue", "fine": 50},
            {"id": 6, "book_id": 6, "user_id": 5, "issue_date": "2024-11-10", "due_date": "2024-11-24", "return_date": None, "status": "Issued", "fine": 0},
            {"id": 7, "book_id": 8, "user_id": 2, "issue_date": "2024-11-12", "due_date": "2024-11-26", "return_date": None, "status": "Issued", "fine": 0},
            {"id": 8, "book_id": 3, "user_id": 4, "issue_date": "2024-09-20", "due_date": "2024-10-04", "return_date": "2024-10-10", "status": "Returned", "fine": 30},
        ],
        "next_book_id": 9,
        "next_user_id": 6,
        "next_transaction_id": 9
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/books")
def books():
    return render_template("books.html")

@app.route("/users")
def users():
    return render_template("users.html")

@app.route("/transactions")
def transactions():
    return render_template("transactions.html")

# ─── API: Dashboard Stats ────────────────────────────────────────────────────

@app.route("/api/stats")
def get_stats():
    data = load_data()
    books = data["books"]
    users = data["users"]
    txns = data["transactions"]

    total_books = sum(b["total_copies"] for b in books)
    available_books = sum(b["available_copies"] for b in books)
    issued_books = total_books - available_books

    active_txns = [t for t in txns if t["status"] in ("Issued", "Overdue")]
    overdue_txns = [t for t in txns if t["status"] == "Overdue"]

    return jsonify({
        "total_books": len(books),
        "total_copies": total_books,
        "available_copies": available_books,
        "issued_copies": issued_books,
        "total_users": len(users),
        "active_users": len([u for u in users if u["status"] == "Active"]),
        "active_transactions": len(active_txns),
        "overdue_transactions": len(overdue_txns),
        "total_transactions": len(txns),
    })

@app.route("/api/recent_transactions")
def get_recent_transactions():
    data = load_data()
    txns = sorted(data["transactions"], key=lambda x: x["issue_date"], reverse=True)[:6]
    enriched = []
    for t in txns:
        book = next((b for b in data["books"] if b["id"] == t["book_id"]), {})
        user = next((u for u in data["users"] if u["id"] == t["user_id"]), {})
        enriched.append({**t, "book_title": book.get("title", "Unknown"), "user_name": user.get("name", "Unknown")})
    return jsonify(enriched)

# ─── API: Books ──────────────────────────────────────────────────────────────

@app.route("/api/books", methods=["GET"])
def get_books():
    data = load_data()
    q = request.args.get("q", "").lower()
    genre = request.args.get("genre", "")
    avail = request.args.get("available", "")
    books = data["books"]
    if q:
        books = [b for b in books if q in b["title"].lower() or q in b["author"].lower() or q in b["isbn"].lower()]
    if genre:
        books = [b for b in books if b["genre"] == genre]
    if avail == "true":
        books = [b for b in books if b["available_copies"] > 0]
    return jsonify(books)

@app.route("/api/books", methods=["POST"])
def add_book():
    data = load_data()
    body = request.json
    new_book = {
        "id": data["next_book_id"],
        "title": body["title"],
        "author": body["author"],
        "genre": body.get("genre", "General"),
        "isbn": body.get("isbn", ""),
        "total_copies": int(body.get("total_copies", 1)),
        "available_copies": int(body.get("total_copies", 1)),
        "added_date": datetime.now().strftime("%Y-%m-%d")
    }
    data["books"].append(new_book)
    data["next_book_id"] += 1
    save_data(data)
    return jsonify(new_book), 201

@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = load_data()
    book = next((b for b in data["books"] if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    body = request.json
    diff = int(body.get("total_copies", book["total_copies"])) - book["total_copies"]
    book.update({
        "title": body.get("title", book["title"]),
        "author": body.get("author", book["author"]),
        "genre": body.get("genre", book["genre"]),
        "isbn": body.get("isbn", book["isbn"]),
        "total_copies": int(body.get("total_copies", book["total_copies"])),
        "available_copies": max(0, book["available_copies"] + diff),
    })
    save_data(data)
    return jsonify(book)

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    data = load_data()
    active = any(t for t in data["transactions"] if t["book_id"] == book_id and t["status"] in ("Issued", "Overdue"))
    if active:
        return jsonify({"error": "Cannot delete book with active transactions"}), 400
    data["books"] = [b for b in data["books"] if b["id"] != book_id]
    save_data(data)
    return jsonify({"success": True})

# ─── API: Users ──────────────────────────────────────────────────────────────

@app.route("/api/users", methods=["GET"])
def get_users():
    data = load_data()
    q = request.args.get("q", "").lower()
    users = data["users"]
    if q:
        users = [u for u in users if q in u["name"].lower() or q in u["email"].lower()]
    return jsonify(users)

@app.route("/api/users", methods=["POST"])
def add_user():
    data = load_data()
    body = request.json
    new_user = {
        "id": data["next_user_id"],
        "name": body["name"],
        "email": body["email"],
        "phone": body.get("phone", ""),
        "member_type": body.get("member_type", "Student"),
        "join_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Active"
    }
    data["users"].append(new_user)
    data["next_user_id"] += 1
    save_data(data)
    return jsonify(new_user), 201

@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = load_data()
    user = next((u for u in data["users"] if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    body = request.json
    user.update({
        "name": body.get("name", user["name"]),
        "email": body.get("email", user["email"]),
        "phone": body.get("phone", user["phone"]),
        "member_type": body.get("member_type", user["member_type"]),
        "status": body.get("status", user["status"]),
    })
    save_data(data)
    return jsonify(user)

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    data = load_data()
    active = any(t for t in data["transactions"] if t["user_id"] == user_id and t["status"] in ("Issued", "Overdue"))
    if active:
        return jsonify({"error": "Cannot delete user with active transactions"}), 400
    data["users"] = [u for u in data["users"] if u["id"] != user_id]
    save_data(data)
    return jsonify({"success": True})

@app.route("/api/users/<int:user_id>/transactions")
def get_user_transactions(user_id):
    data = load_data()
    txns = [t for t in data["transactions"] if t["user_id"] == user_id]
    enriched = []
    for t in txns:
        book = next((b for b in data["books"] if b["id"] == t["book_id"]), {})
        enriched.append({**t, "book_title": book.get("title", "Unknown")})
    return jsonify(enriched)

# ─── API: Transactions ───────────────────────────────────────────────────────

@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    data = load_data()
    status = request.args.get("status", "")
    txns = data["transactions"]
    if status:
        txns = [t for t in txns if t["status"] == status]
    enriched = []
    for t in sorted(txns, key=lambda x: x["issue_date"], reverse=True):
        book = next((b for b in data["books"] if b["id"] == t["book_id"]), {})
        user = next((u for u in data["users"] if u["id"] == t["user_id"]), {})
        enriched.append({**t, "book_title": book.get("title", "Unknown"), "user_name": user.get("name", "Unknown")})
    return jsonify(enriched)

@app.route("/api/transactions/issue", methods=["POST"])
def issue_book():
    data = load_data()
    body = request.json
    book_id = int(body["book_id"])
    user_id = int(body["user_id"])

    book = next((b for b in data["books"] if b["id"] == book_id), None)
    user = next((u for u in data["users"] if u["id"] == user_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if not user:
        return jsonify({"error": "User not found"}), 404
    if book["available_copies"] < 1:
        return jsonify({"error": "No copies available"}), 400

    already_issued = any(
        t for t in data["transactions"]
        if t["book_id"] == book_id and t["user_id"] == user_id and t["status"] in ("Issued", "Overdue")
    )
    if already_issued:
        return jsonify({"error": "User already has this book issued"}), 400

    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=14)
    txn = {
        "id": data["next_transaction_id"],
        "book_id": book_id,
        "user_id": user_id,
        "issue_date": issue_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "return_date": None,
        "status": "Issued",
        "fine": 0
    }
    data["transactions"].append(txn)
    data["next_transaction_id"] += 1
    book["available_copies"] -= 1
    save_data(data)
    return jsonify({**txn, "book_title": book["title"], "user_name": user["name"]}), 201

@app.route("/api/transactions/<int:txn_id>/return", methods=["POST"])
def return_book(txn_id):
    data = load_data()
    txn = next((t for t in data["transactions"] if t["id"] == txn_id), None)
    if not txn:
        return jsonify({"error": "Transaction not found"}), 404
    if txn["status"] == "Returned":
        return jsonify({"error": "Book already returned"}), 400

    return_date = datetime.now()
    due_date = datetime.strptime(txn["due_date"], "%Y-%m-%d")
    fine = 0
    if return_date > due_date:
        overdue_days = (return_date - due_date).days
        fine = overdue_days * 5  # ₹5/day

    txn["return_date"] = return_date.strftime("%Y-%m-%d")
    txn["status"] = "Returned"
    txn["fine"] = fine

    book = next((b for b in data["books"] if b["id"] == txn["book_id"]), None)
    if book:
        book["available_copies"] = min(book["available_copies"] + 1, book["total_copies"])

    save_data(data)
    return jsonify({**txn, "fine": fine})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
