# LibraryOS — Library Management System

A full-stack web application built with **Python (Flask)** + **HTML/CSS/JavaScript**.

---

## Features

- **Dashboard** — live stats: books, members, transactions, overdue count
- **Books** — add, edit, delete, search, filter by genre, availability toggle
- **Members** — register, edit, remove, view transaction history per member
- **Transactions** — issue books, process returns, fine calculation (₹5/day overdue)
- Data persisted in `data.json` (no database required)

---

## Quick Start

### Prerequisites
- Python 3.8+ installed

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
python app.py
```

### 3. Open in browser

```
http://localhost:5000
```

---

## Project Structure

```
library_management_system/
├── app.py                  ← Flask backend (all API routes)
├── requirements.txt        ← Python dependencies
├── data.json               ← Auto-created on first run (data store)
├── templates/
│   ├── base.html           ← Shared layout (sidebar, topbar, modal, toast)
│   ├── index.html          ← Dashboard page
│   ├── books.html          ← Books management page
│   ├── users.html          ← Members management page
│   └── transactions.html   ← Transactions page (issue/return)
└── static/
    ├── css/
    │   └── style.css       ← All styles (dark theme, responsive)
    └── js/
        └── main.js         ← Shared JS (api helper, modal, toast)
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Dashboard statistics |
| GET | `/api/books` | List books (supports `?q=`, `?genre=`, `?available=true`) |
| POST | `/api/books` | Add a new book |
| PUT | `/api/books/<id>` | Update a book |
| DELETE | `/api/books/<id>` | Delete a book |
| GET | `/api/users` | List members (supports `?q=`) |
| POST | `/api/users` | Register a new member |
| PUT | `/api/users/<id>` | Update a member |
| DELETE | `/api/users/<id>` | Remove a member |
| GET | `/api/users/<id>/transactions` | Member's transaction history |
| GET | `/api/transactions` | List transactions (supports `?status=`) |
| POST | `/api/transactions/issue` | Issue a book |
| POST | `/api/transactions/<id>/return` | Return a book |

---

## Fine Policy

- Loan period: **14 days**
- Fine for late return: **₹5 per day**

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Data | JSON file (no database needed) |
| Fonts | DM Serif Display, Inter, JetBrains Mono |
