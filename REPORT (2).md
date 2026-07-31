# Project Report — Card Catalog Notes App (Flask + SQLite)

**Intern:** Abdullah Arif
**Internship:** Synent Technologies — Python Development Internship
**Task:** Task 9 — Advanced Level
**Repository:** synent-task9-notesapp-abdullaharif

---

## 1. Objective

To build a full-stack web application using Flask, featuring user authentication (registration, login, session handling) and a core CRUD feature — in this case, a personal Notes app — backed by a SQLite database, with a simple, responsive UI.

## 2. Requirements Covered

| Requirement | Status |
|---|---|
| User Registration & Login | ✅ |
| Session handling | ✅ |
| Core functionality (Notes App chosen) | ✅ |
| Database storing user data and records | ✅ (SQLite) |
| Simple, responsive UI | ✅ |
| Fully working web application | ✅ |

## 3. Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (via Python's built-in `sqlite3` module)
- **Frontend:** HTML (Jinja2 templates) + custom CSS — no external frontend framework
- **Security:** Werkzeug's password hashing utilities (`generate_password_hash`, `check_password_hash`)

## 4. Methodology / Approach

### 4.1 Database Design
Two tables were designed in `database.py`:
- **`users`** — stores `id`, `username` (unique), `password_hash`, `created_at`
- **`notes`** — stores `id`, `user_id` (foreign key to `users`), `title`, `content`, `created_at`, `updated_at`

The foreign key uses `ON DELETE CASCADE`, so if a user were ever deleted, their notes would be cleaned up automatically rather than becoming orphaned data.

### 4.2 Authentication & Session Handling
- Passwords are **never stored in plain text** — they are hashed using Werkzeug's PBKDF2-based `generate_password_hash()` before being saved, and verified with `check_password_hash()` on login.
- On successful login, `session["user_id"]` and `session["username"]` are set using Flask's built-in signed-cookie session mechanism.
- A custom `@login_required` decorator wraps every note-related route (dashboard, new note, edit, delete). If no `user_id` is present in the session, the user is redirected to the login page with a flash message.
- Registration includes validation: minimum username length (3), minimum password length (6), and a password-confirmation match check, along with a duplicate-username check against the database.

### 4.3 Core CRUD Functionality (Notes)
- **Create** — `/notes/new` renders a form and inserts a new row into `notes`, tied to `session["user_id"]`.
- **Read** — `/dashboard` queries only the notes belonging to the logged-in user (`WHERE user_id = ?`), ordered by most recently updated.
- **Update** — `/notes/<id>/edit` fetches the note *and* checks it belongs to the current user before allowing edits.
- **Delete** — `/notes/<id>/delete` similarly checks ownership before deleting.

This ownership check on every read/update/delete operation was a deliberate security measure to prevent one user from accessing or modifying another user's notes simply by guessing or incrementing note IDs in the URL.

### 4.4 Frontend / UI
The interface was built with server-rendered Jinja2 templates and a custom stylesheet (no Bootstrap/Tailwind), themed around a "library card catalog" concept — notes are visually presented as index cards with ruled lines and a punched tab label, using a navy/brass/paper color palette. The layout is responsive down to mobile screen widths using CSS Grid and media queries.

## 5. Testing Performed

The application was tested using Flask's built-in test client (automated, scripted tests) as well as by running the actual development server and interacting with it in a browser:

- **Registration validation:** duplicate username, short username, short password, mismatched passwords — all correctly rejected with appropriate error messages.
- **Login:** correct credentials succeed; incorrect password is rejected with a generic error message (to avoid leaking which part was wrong).
- **Auth protection:** accessing `/dashboard` or any note route without being logged in correctly redirects to the login page.
- **CRUD operations:** notes can be created, edited, and deleted successfully; the dashboard correctly reflects an empty state when a user has no notes.
- **Cross-user security test:** created a note as "User A," then logged in as "User B" and attempted to view, edit, and delete User A's note by directly guessing/using its note ID in the URL. In all cases, access was correctly blocked, confirming notes are properly isolated per user.
- **Logout:** confirmed the session is cleared and protected pages become inaccessible again afterward.
- **Live server check:** ran `python app.py` and confirmed the login and registration pages return the correct HTTP status codes and render properly in a browser.

## 6. Output

A fully working, locally-runnable web application where users can register, log in, and manage a private set of notes through a clean, responsive interface — with data persisted in a SQLite database file (`notes_app.db`) that is created automatically on first run.

## 7. Conclusion

This was the most comprehensive task of the three, combining backend routing, database design, authentication/session security, and frontend design into a single working application. Particular care was taken around password security and per-user data isolation, since these are common real-world vulnerabilities in web applications if not handled explicitly.
