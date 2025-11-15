[![Static Badge](https://img.shields.io/badge/flask-app_base-blue)](https://github.com/wiley-man/Flask-App-Base)
[![GitHub License](https://img.shields.io/github/license/wiley-man/flask-app-base)](https://github.com/wiley-man/Flask-App-Base/blob/main/LICENSE)
[![GitHub Release](https://img.shields.io/github/v/release/wiley-man/flask-app-base)](https://github.com/wiley-man/Flask-App-Base/releases/tag/v1.2.0)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/wiley-man/flask-app-base/flask-app.yml?branch=main&event=push&logoSize=auto&color=lightgreen)](https://github.com/wiley-man/Flask-App-Base/actions)
[![Static Badge](https://img.shields.io/badge/python-3.11-purple?logo=python&logoSize=auto)](https://www.python.org/downloads/release/python-31114/)
[![Static Badge](https://img.shields.io/badge/flask-3.1-purple?logo=flask&logoSize=auto)](https://flask.palletsprojects.com/en/stable/)

---

# Flask App Base

## 📚 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [How the Flask App Base Works](#how-the-flask-app-base-works)

---

## Project Overview
A clean, battle-tested Flask application structure using the app‑factory pattern, environment configuration, SQLAlchemy, Flask‑Migrate, Blueprints, WTForms, and modular templates/static files.

This project provides a production-ready baseline for Flask applications with clear separation of concerns and strong testing support.

---

## 🚀 Features

- **App Factory Architecture**  
  Scalable, maintainable initialization using `create_app()` across all environments.

- **Environment-Based Configuration**  
  Includes `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig`, with layered loading from `.env`, instance configs, and external settings files.

- **SQLAlchemy ORM Integration**  
  Full database support using SQLAlchemy models and session management.

- **Flask-Migrate Support**  
  Database migrations powered by Alembic using `flask db migrate` and `flask db upgrade`.

- **Blueprint Routing System**  
  Modular routing with Flask Blueprints for clean organization as the project grows.

- **Secure Configuration Layering**  
  Config sourced from environment variables, config classes, instance config, and optional `YOURAPP_SETTINGS`.

- **WTForms + Flask-WTF Integration**  
  Built-in form handling with CSRF protection, validation, field classes, and rendering helpers for creating secure and interactive user forms.

- **WSGI Production Entrypoint**  
  Deploy-ready via Gunicorn, uWSGI, or shared hosting platforms using `wsgi.py`.

- **Built-In Logging Configuration**  
  Environment-aware logging with configurable log levels.

- **Testing with Pytest and coverage**  
  Fully integrated testing setup using `pytest` for fast, isolated test execution and `coverage` for measuring code quality, ensuring your application remains reliable and well-tested as it grows.

- **Clean, Organized Project Structure**  
  Well-organized templates, static assets, blueprints, and extensions suitable as a reliable foundation for new Flask applications.

---

# Project Structure
```
flaskapp/
├── __init__.py
├── config.py
├── extensions.py
├── models.py
├── routes.py
├── templates/
├── static/
tests/
├── conftest.py
├── test_models.py
wsgi.py
```

---

## 🧠 How the Flask App Base Works

Think of this project less as a “starter app” and more as a **minimal architecture** for serious Flask work. It’s built around the **app-factory pattern**, **layered configuration**, **extensions**, and **blueprints** to avoid the usual pain points: circular imports, untestable code, and configuration drift between environments.

Below is the fully expanded version including ASCII diagrams, explanations, and rationale behind each architectural decision.

---

### 🧱 Architecture Overview

```text
                 ┌──────────────────────────────┐
                 │        wsgi.py (Prod)        │
                 │    WSGI Entrypoint Module    │
                 └──────────────┬───────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │  create_app() Factory   │
                    │  (flaskapp/__init__.py) │
                    └──────────────┬──────────┘
                                   │
         ┌─────────────────────────┼──────────────────────────┐
         ▼                         ▼                          ▼
┌─────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│ Load Config     │     │ Init Extensions    │     │ Register Blueprints│
│ - Base Config   │     │ - SQLAlchemy (db)  │     │ - main_bp          │
│ - Env Config    │     │ - Flask-Migrate    │     │ - api_bp (opt)     │
│ - Instance cfg  │     │ - Flask-WTF/WTForms│     │ - auth_bp (opt)    │
└─────────────────┘     └────────────────────┘     └────────────────────┘
                                   │
                                   ▼
                     ┌─────────────────────────┐
                     │   Application Ready     │
                     │   (Flask app object)    │
                     └─────────────────────────┘

     ┌─────────────────────────────────────────────────────────────┐
     │                    RUNTIME EXECUTION                        │
     │  HTTP Request → Routing → View → Template/JSON → Response   │
     └─────────────────────────────────────────────────────────────┘
```

---

### 🔧 App Factory Lifecycle

```text
┌───────────────────────────────────────────────────────────┐
│                  create_app(config_name)                  │
└───────────────┬───────────────────────────────────────────┘
                │
                ▼
       ┌─────────────────────────────┐
       │ Determine config target     │
       │ - if config_name is passed  │
       │ - else use FLASK_ENV_NAME   │
       └───────────────┬─────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ Load Base Config        │
          │  (Config)               │
          └─────────────┬───────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │ Load Env Config Class   │
          │ (Development/Testing/   │
          │  Production)            │
          └─────────────┬───────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │ Load instance/config.py │
          │ (optional, per-machine) │
          └─────────────┬───────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │ Load YOURAPP_SETTINGS   │
          │ file (optional)         │
          └─────────────┬───────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │ Initialize Extensions   │
          │ - db.init_app(app)      │
          │ - migrate.init_app(...) │
          │ - Flask-WTF/CSRF setup  │
          └─────────────┬───────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │ Register Blueprints     │
          │ - main_bp, api_bp, ...  │
          └─────────────┬───────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │ Configure Logging       │
          │ (LOG_LEVEL, handlers)   │
          └─────────────┬───────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │  return app             │
          └─────────────────────────┘
```

---

### 1️⃣ Why the App Factory Pattern Exists

A naïve Flask app initializes the application at import time:

```python
app = Flask(__name__)
```

This causes problems:

- Cannot create isolated app instances for testing
- Tight coupling of imports → circular import issues
- Hard to dynamically switch environments
- Extensions initialize too early

**The factory pattern fixes all of this:**

```python
def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)
    return app
```

By deferring initialization:

- Configuration selection happens at runtime.
- Extensions initialize safely.
- Blueprints register cleanly.
- Tests can spin up isolated applications.

---

### 2️⃣ Layered Configuration System

Config loads in an intentional sequence:

1. **Base Config (`Config`)**  
   Default values: SESSION settings, tracking flags, DB fallback.

2. **Environment-Specific Config**  
   - `DevelopmentConfig`
   - `TestingConfig`
   - `ProductionConfig`

3. **Instance Config (`instance/config.py`)**  
   Private machine-specific settings, ignored by Git.

4. **`YOURAPP_SETTINGS` external file**  
   Allows ops to override configs without editing source.

> [!WARNING]
> instance/config.py is meant to handler credential and secrects
> best practice would be put the instance directory in the projects
> .gitignore file or use the YOURAPP_SETTINGS enviorment variable
> to move the config.py file outside of the project directory.

This layering provides predictable overrides and clean separation of environments.

---

### 3️⃣ Extension Initialization (Avoiding Circular Imports)

Extensions are instantiated once globally:

```python
db = SQLAlchemy()
migrate = Migrate()
```

Then initialized inside `create_app()`:

```python
db.init_app(app)
migrate.init_app(app, db)
```

Models import `db` from `extensions.py` rather than from the Flask app itself — a critical anti-circular-import measure.

---

### 4️⃣ Scalability Through Blueprints

Blueprints keep routing modular:

- `main` → public pages
- `api` → JSON endpoints
- `auth` → login/registration
- `admin` → dashboards

Each blueprint contains its own views, templates, and static files.  
They are attached in a single place: the app factory.

---

### 5️⃣ Database Layer – SQLAlchemy + Flask-Migrate

Provides:

- ORM models
- Relationship mapping
- Alembic-powered migrations
- Reversible schema evolution

This avoids manually altering schema or destroying data between updates.

---

### 6️⃣ Testing with Pytest + In-Memory Database

Because the app factory accepts a config name:

```python
app = create_app("testing")
```

The testing environment provides:

- **SQLite in-memory database**
- **CSRF disabled (optional)**
- **TESTING=True**

Fixtures can:

- create an app
- push the app context
- create tables
- yield a client and session
- tear down everything cleanly

This produces fast, deterministic tests.

---

### 7️⃣ WSGI Entrypoint for Production Deployment

```python
from flaskapp import create_app
app = create_app()
```

Gunicorn, uWSGI, or other WSGI servers load this file, allowing:

- zero code changes between environments
- config switching via environment variables
- stable deploy behavior

---

### 🎯 Summary

This architecture provides:

- Predictable environment behavior  
- No circular imports  
- Modular routing via blueprints  
- Testability by design  
- Safe extension initialization  
- Clean deployment through WSGI  

Small enough to learn quickly, but strong enough for production.