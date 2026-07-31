# 🗂️ Card Catalog — Notes App (Flask + SQLite)

**Synent Technologies Internship — Task 9 (Advanced Level)**

A full-stack notes application built with Flask and SQLite, featuring user authentication with session handling and complete CRUD functionality for personal notes. Each note is rendered in the UI as a library index card, styled around a card-catalog visual theme.

## ✨ Features

**Authentication**
- User registration with validation (username length, password length, confirm-password match)
- Secure password storage using Werkzeug's `generate_password_hash` / `check_password_hash` (passwords are never stored in plain text)
- Session-based login/logout
- `login_required` decorator protecting all note routes — no note is accessible without being signed in

**Notes (Core Functionality)**
- Create, read, update, and delete personal notes
- Notes are scoped per user — a user can only ever see, edit, or delete their **own** notes (verified in testing, including direct URL/ID tampering attempts)
- Empty-state screen when a user has no notes yet
- Delete confirmation prompt before removing a note

**Database**
- SQLite (`notes_app.db`), created automatically on first run
- Two tables: `users` and `notes`, linked by foreign key with `ON DELETE CASCADE`

**UI**
- Clean, responsive, server-rendered interface (Jinja2 templates + custom CSS, no frontend framework required)
- Distinctive "library card catalog" design: notes styled as index cards with ruled lines and a punched tab label
- Flash messages for success/error feedback (registration errors, invalid login, note validation, etc.)
- Accessible: visible keyboard focus states, respects `prefers-reduced-motion`

## 📦 Requirements

- Python 3.7+
- Flask, Werkzeug (see `requirements.txt`)

## 🚀 Setup & Usage

```bash
# 1. Clone the repo and enter the folder
cd synent-task9-notesapp-yourname

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize the database (creates notes_app.db)
python database.py

# 5. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

1. Register a new account
2. Log in
3. Create, edit, and delete notes from your dashboard
4. Log out when done

## 🏗️ Project Structure

```
synent-task9-notesapp-yourname/
│
├── app.py                # Flask application: routes, auth, CRUD logic
├── database.py            # SQLite connection + schema setup
├── requirements.txt        # Python dependencies
├── .gitignore
├── static/
│   └── style.css          # Card-catalog design system
└── templates/
    ├── base.html           # Shared layout, header, flash messages
    ├── login.html
    ├── register.html
    ├── dashboard.html      # Lists notes as index cards
    └── note_form.html      # Shared create/edit form
```

## 🔐 Security Notes

- Passwords are hashed with Werkzeug's PBKDF2-based hashing before storage — never stored or logged in plain text.
- The Flask `secret_key` in `app.py` is a placeholder (`"dev-secret-key-change-this-in-production"`) and should be replaced with a securely generated value before any real deployment (e.g. via an environment variable).
- All note routes check that the note's `user_id` matches the logged-in user's session ID before allowing read/edit/delete — this was explicitly tested to prevent one user from tampering with another user's notes via direct URL access.

## 🧪 Testing Performed

This app was tested end-to-end using Flask's test client, covering:
- Registration (including duplicate username, short username, short password, mismatched passwords)
- Login (correct credentials, wrong password)
- Auth protection (dashboard/notes unreachable without logging in)
- Full CRUD on notes (create, edit, delete, empty-state rendering)
- Cross-user isolation (User B cannot view, edit, or delete User A's notes by guessing note IDs)
- Logout (session properly cleared)

## 👤 Author

**Abdullah Arif** — Synent Technologies Python Programming Internship

---
*Tagged: @Synent Technologies | #internship #python #programming #technology*
