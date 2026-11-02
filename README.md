# Flask Blogging Platform

[![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-blue?style=flat&logo=python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red?style=flat)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-59%20Passed-brightgreen)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A full-featured, scalable blogging platform built with **Python**, **Flask**, **Flask-SQLAlchemy**, **Flask-Migrate**, **Flask-Login**, **Flask-WTF**, and **Jinja2**. Developed for the **DIY Internship Program**.

---

## 📅 Internship Roadmap & Milestone Deliverables

### ✅ Week 1: Flask Setup and Basic Structure
- **Flask Environment:** Application Factory pattern configured in `app/__init__.py` supporting `development`, `testing`, and `production`.
- **Blueprints Architecture:** Modular routing split into `main`, `auth`, and `posts`.
- **Database Models (SQLAlchemy):** Relational schema for `User`, `Post`, `Category`, `Tag` (Many-to-Many), and `Comment`.
- **Database Migrations:** Managed using `Flask-Migrate` and `Alembic`.

### ✅ Week 2: User Authentication & Profiles
- **User Authentication:** Registration, Secure Password Hashing (Werkzeug), and Login/Logout management with `Flask-Login`.
- **Session Management:** Secure cookie-based session handling, `remember_me` functionality, and `@login_required` decorators.
- **User Profiles:** Author profile pages showcasing bio, avatar, joined date, and published articles.
- **Profile Customization:** Profile editing with avatar URL and biography updates.

### ✅ Week 3: Blog Post CRUD
- **Create, Read, Update, Delete (CRUD):** Complete post lifecycle with authorization guards.
- **Rich Text Editor:** Integrated Quill.js rich text editor with sanitized HTML rendering.
- **Slug Generation & Uniqueness:** Automatic URL-friendly slug generation with duplicate resolution.
- **Taxonomy:** Categories and tags tagging system with dynamic creation.

### ✅ Week 4: Frontend: Displaying Posts, Navigation, and Pagination
- **Jinja2 Templates:**
  - Modern Home page with Hero section, latest articles, categories, and tags.
  - Dedicated individual post view (`detail.html`) with breadcrumbs, author profile link, reading time, and formatted dates.
  - User profile page with paginated articles list.
- **Pagination:** Efficient database-level pagination across homepage, articles list, and author profiles.
- **Responsive Navigation:** Interactive navbar with active route highlighting, user dropdown, and quick post creation CTA.

### ✅ Week 5: Commenting System
- **Interactive Comments:** Authenticated users can leave comments directly on blog articles.
- **Validation:** Input length checks, CSRF protection, and error messaging.
- **Moderation & Permissions:**
  - Comment author can delete their own comments.
  - Post author can moderate/delete any comment on their articles.
  - Unauthorized users are restricted (HTTP 403 Forbidden).
- **Cascade Deletions:** Deleting a post automatically cleans up all associated comments.

### ✅ Week 6: Search and Filtering
- **Full-Text Keyword Search:** Search posts by title, summary, or content using SQLAlchemy `ilike` pattern matching.
- **Taxonomy Filters:** Filter articles by category or tag.
- **Combined Queries:** Seamlessly combine keyword searches with category and tag filters.
- **Navbar Search:** Global search bar in navigation bar and dedicated search box in articles view.
- **Active Filter Pills & Reset:** Clear visualization of applied filters and instant reset options.

### ✅ Week 7: Deployment Preparation and Comprehensive Testing
- **Automated Test Suite:** 59 comprehensive unit tests covering:
  - Basic routes & error handling (`test_basic.py`)
  - User authentication, registration & profiles (`test_auth.py`)
  - Post CRUD, permissions & slug generation (`test_posts.py`)
  - Comment creation, authorization & cascade deletion (`test_comments.py`)
  - Keyword search, category/tag filtering & combinations (`test_search.py`)
  - Deployment configuration & healthchecks (`test_deployment.py`)
- **Dockerization:** Production-ready `Dockerfile` based on `python:3.11-slim` with built-in healthchecks.
- **Multi-Container Orchestration:** `docker-compose.yml` with persistent database volume.
- **Production WSGI Server:** Configured with `Gunicorn` and `wsgi.py` entrypoint.
- **Healthcheck Endpoint:** `/health` endpoint returning system status for container orchestrators.

---

## 📂 Project Directory Structure

```text
flask-blogging-platform/
├── app/
│   ├── __init__.py           # Application Factory (create_app)
│   ├── config.py             # Development, Testing, and Production configs
│   ├── extensions.py         # SQLAlchemy, Migrate, LoginManager, CSRFProtect
│   ├── blueprints/
│   │   ├── main/             # Home, About, Health routes
│   │   ├── auth/             # Login, Register, Profile routes & forms
│   │   └── posts/            # Post CRUD, Comments, Search routes & forms
│   ├── models/
│   │   ├── __init__.py       # Model exports
│   │   ├── user.py           # User model & password hashing
│   │   ├── post.py           # Post, Category, Tag models
│   │   └── comment.py        # Comment model
│   ├── static/
│   │   └── css/
│   │       └── style.css     # Responsive design system
│   └── templates/
│       ├── base.html         # Base Jinja2 layout with Navbar & Search
│       ├── errors/           # Custom 404 & 500 error pages
│       ├── main/             # Home & About pages
│       ├── auth/             # Login, Register, Profile, Edit Profile
│       └── posts/            # List, Detail (with Comments), Create, Edit
├── migrations/               # Alembic database migration scripts
├── tests/
│   ├── test_basic.py         # Basic routes & config tests
│   ├── test_auth.py          # Authentication & user tests
│   ├── test_posts.py         # Post CRUD & pagination tests
│   ├── test_comments.py      # Commenting system tests
│   ├── test_search.py        # Search & filtering tests
│   └── test_deployment.py    # Healthcheck & deployment tests
├── Dockerfile                # Production Docker container definition
├── docker-compose.yml        # Docker Compose configuration
├── .dockerignore             # Docker build context exclusions
├── wsgi.py                   # Production Gunicorn WSGI entrypoint
├── requirements.txt          # Python dependencies
├── run.py                    # Local development runner
├── seed.py                   # Database sample data seeder
└── README.md                 # Complete documentation
```

---

## 🚀 Getting Started

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/shubh-2102/flask-blogging-platform.git
cd flask-blogging-platform
```

#### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run Database Migrations or Seed Data
```bash
# Apply database migrations
flask db upgrade

# (Optional) Seed with sample categories, tags, and posts
python seed.py
```

#### 5. Start the Development Server
```bash
python run.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🐳 Running with Docker & Docker Compose

### Using Docker Compose (Recommended)
```bash
# Build and run the container
docker compose up --build -d

# View container logs
docker compose logs -f

# Check health status
curl http://localhost:5000/health

# Stop containers
docker compose down
```

### Using Docker Standalone
```bash
# Build Docker image
docker build -t flask-blog .

# Run container
docker run -p 5000:5000 -e SECRET_KEY="my-secret-key" flask-blog
```

---

## 🧪 Running Automated Tests

Run the full automated test suite using Python's standard `unittest` framework:

```bash
# Run all tests
python -m unittest discover tests

# Or run specific test modules
python -m unittest tests.test_basic
python -m unittest tests.test_auth
python -m unittest tests.test_posts
python -m unittest tests.test_comments
python -m unittest tests.test_search
python -m unittest tests.test_deployment
```

All **59 tests** run with 100% pass rate in an isolated in-memory SQLite database environment.

---

## 🛡️ License

This project is licensed under the MIT License.
