"""
app.py
-------
Full-stack Notes App built with Flask + SQLite.

Features:
- User registration & login (session-based auth, hashed passwords)
- Create / Read / Update / Delete notes, scoped to the logged-in user
- Simple, responsive UI (server-rendered Jinja2 templates)

Author: Abdullah Arif
Task: Synent Technologies Internship - Task 9 (Advanced)
"""

from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-this-in-production"  # Replace before deploying


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def login_required(view_func):
    """Decorator that redirects to the login page if no user is in session."""
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped_view


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        error = None
        if not username or not password:
            error = "Username and password are required."
        elif len(username) < 3:
            error = "Username must be at least 3 characters long."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        elif password != confirm_password:
            error = "Passwords do not match."

        if error is None:
            conn = get_db_connection()
            existing = conn.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()

            if existing is not None:
                error = f"Username '{username}' is already taken."
            else:
                conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                conn.commit()
                conn.close()
                flash("Account created successfully. Please log in.", "success")
                return redirect(url_for("login"))
            conn.close()

        flash(error, "error")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# Notes CRUD routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()
    notes = conn.execute(
        "SELECT * FROM notes WHERE user_id = ? ORDER BY updated_at DESC",
        (session["user_id"],),
    ).fetchall()
    conn.close()
    return render_template("dashboard.html", notes=notes)


@app.route("/notes/new", methods=["GET", "POST"])
@login_required
def new_note():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Both title and content are required.", "error")
            return render_template("note_form.html", note=None, form_action=url_for("new_note"))

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)",
            (session["user_id"], title, content),
        )
        conn.commit()
        conn.close()
        flash("Note created.", "success")
        return redirect(url_for("dashboard"))

    return render_template("note_form.html", note=None, form_action=url_for("new_note"))


@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    conn = get_db_connection()
    note = conn.execute(
        "SELECT * FROM notes WHERE id = ? AND user_id = ?",
        (note_id, session["user_id"]),
    ).fetchone()

    if note is None:
        conn.close()
        flash("Note not found.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Both title and content are required.", "error")
            conn.close()
            return render_template(
                "note_form.html", note=note, form_action=url_for("edit_note", note_id=note_id)
            )

        conn.execute(
            "UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP "
            "WHERE id = ? AND user_id = ?",
            (title, content, note_id, session["user_id"]),
        )
        conn.commit()
        conn.close()
        flash("Note updated.", "success")
        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("note_form.html", note=note, form_action=url_for("edit_note", note_id=note_id))


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM notes WHERE id = ? AND user_id = ?",
        (note_id, session["user_id"]),
    )
    conn.commit()
    conn.close()
    flash("Note deleted.", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
