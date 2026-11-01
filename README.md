# Flask Blogging Platform

[![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat&logo=python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red?style=flat)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A full-featured, scalable blogging platform built with **Python**, **Flask**, **Flask-SQLAlchemy**, **Flask-Migrate**, and **Jinja2**. This project is developed as part of the **DIY Internship Program**.

---

## 📅 Internship Progress: Week 1 Deliverables

### **Week 1: Flask Setup and Basic Structure**
- [x] **Flask Environment Setup:** Python virtual environment with dependencies managed via `requirements.txt`.
- [x] **Application Factory Pattern:** Created `create_app()` in `app/__init__.py` supporting development, testing, and production environments.
- [x] **Modular Architecture with Blueprints:**
  - `main`: Homepage, About, and error handlers.
  - `auth`: Authentication routes (login, register, logout placeholders).
  - `posts`: Blog article browsing and detail views.
- [x] **Database Configuration & Models (SQLAlchemy):**
  - `User`: Account details, password hashing (Werkzeug), and relationships.
  - `Post`: Article title, slug, content, published status, timestamps, and authorship.
  - `Category`: Categorization for articles.
  - `Tag`: Many-to-many tag mapping via `post_tags` association table.
  - `Comment`: User comments on articles.
- [x] **Database Migrations (Flask-Migrate & Alembic):** Configured and executed initial migration scripts.
- [x] **Automated Unit Tests:** Test suite verifying application creation, routes, password hashing, and ORM relationships.
- [x] **Responsive UI:** Modern styling with clean typography, cards, badges, and responsive layouts.

---

## 📂 Project Directory Structure

```text
flask-blogging-platform/
├── app/
│   ├── __init__.py           # Application Factory (create_app)
│   ├── config.py             # Development, Testing, and Production configs
│   ├── extensions.py         # SQLAlchemy, Migrate, LoginManager, CSRFProtect
│   ├── blueprints/
│   │   ├── main/             # Home and general routes
│   │   ├── auth/             # Authentication routes
│   │   └── posts/            # Blog posts routes
│   ├── models/
│   │   ├── __init__.py       # Model exports
│   │   ├── user.py           # User model & password hashing
│   │   ├── post.py           # Post, Category, Tag models
│   │   └── comment.py        # Comment model
│   ├── static/
│   │   └── css/
│   │       └── style.css     # Responsive design system
│   └── templates/
│       ├── base.html         # Base Jinja2 layout
│       ├── errors/           # Custom 404 & 500 error pages
│       ├── main/             # Index & About pages
│       ├── auth/             # Login & Register views
│       └── posts/            # Post list & detail views
├── migrations/               # Alembic database migration scripts
├── tests/
│   └── test_basic.py         # Unit tests suite
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
├── seed.py                   # Initial demo database seeder
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/shubh-2102/flask-blogging-platform.git
cd flask-blogging-platform
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
copy .env.example .env   # Windows
# or
cp .env.example .env    # Linux / macOS
```

### 5. Apply Database Migrations
```bash
flask db upgrade
```

### 6. (Optional) Seed Initial Data
```bash
python seed.py
```

### 7. Run the Application
```bash
python run.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🧪 Running Unit Tests

Run the test suite to ensure all blueprints, routes, and models are functioning properly:
```bash
python -m unittest discover tests
```

---

## 🗺️ Upcoming Milestones

- **Week 2:** User Authentication (Flask-Login, Flask-WTF forms, CSRF validation, user profiles).
- **Week 3:** Post CRUD operations, Rich Text Editor integration, image uploads, and tagging.
- **Week 4:** Interactive commenting system, full-text search, UI polish, and production deployment.
