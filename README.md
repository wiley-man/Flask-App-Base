```{=html}
<!-- Badges -->
```
```{=html}
<p align="center">
```
`<a href="https://github.com/wiley-man/Flask-App-Base">`{=html}`<img src="https://img.shields.io/badge/Flask-App%20Base-blue?style=flat-square" alt="Project Badge">`{=html}`</a>`{=html}
`<a href="https://github.com/wiley-man/Flask-App-Base/actions">`{=html}`<img src="https://img.shields.io/github/actions/workflow/status/wiley-man/Flask-App-Base/test.yml?style=flat-square&label=Tests" alt="Build Status">`{=html}`</a>`{=html}
`<a href="https://github.com/wiley-man/Flask-App-Base/blob/main/LICENSE">`{=html}`<img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License">`{=html}`</a>`{=html}
`<img src="https://img.shields.io/badge/Python-3.11%2B-blueviolet?style=flat-square" alt="Python Version">`{=html}
`<img src="https://img.shields.io/badge/Flask-3.1-lightgrey?style=flat-square" alt="Flask Version">`{=html}
```{=html}
</p>
```

------------------------------------------------------------------------

# Flask App Base

A clean and battle-tested Flask application template featuring the
app-factory pattern, environment-based configuration, and clear
separation of development, testing, and production settings.

## 🚀 Features

-   **App Factory Architecture**\
    Scalable, maintainable initialization using `create_app()` across
    all environments.

-   **Environment-Based Configuration**\
    Includes `DevelopmentConfig`, `TestingConfig`, and
    `ProductionConfig`, with layered loading from `.env`, instance
    configs, and external settings files.

-   **SQLAlchemy ORM Integration**\
    Full database support using SQLAlchemy models and session
    management.

-   **Flask-Migrate Support**\
    Database migrations powered by Alembic using `flask db migrate` and
    `flask db upgrade`.

-   **Blueprint Routing System**\
    Modular routing with Flask Blueprints for clean organization as the
    project grows.

-   **Secure Configuration Layering**\
    Config sourced from environment variables, config classes, instance
    config, and optional `YOURAPP_SETTINGS`.

-   **WSGI Production Entrypoint**\
    Deploy-ready via Gunicorn, uWSGI, or shared hosting platforms using
    `wsgi.py`.

-   **Built-In Logging Configuration**\
    Environment-aware logging with configurable log levels.

-   **Testing Support with Pytest**\
    Includes fixtures for app creation, test client, and an in-memory
    SQLite database for fast, isolated tests.

-   **Clean, Organized Project Structure**\
    Well-organized templates, static assets, blueprints, and extensions
    suitable as a reliable foundation for new Flask applications.

------------------------------------------------------------------------

## 📁 Project Structure

The project is organized using a clean, scalable layout that separates
configuration, core application code, instance-specific settings, and
tests.

    flask-app-base/
    ├─ flaskapp/
    │  ├─ templates/
    │  ├─ static/
    │  ├─ __init__.py
    │  ├─ extensions.py
    │  ├─ routes.py
    │  ├─ models.py
    │  └─ config.py
    ├─ instance/
    │  └─ config.py
    ├─ tests/
    │  ├─ conftest.py
    │  ├─ test_main.py
    │  └─ test_database.py
    ├─ .env
    ├─ .env.test
    ├─ requirements.txt
    ├─ wsgi.py
    └─ README.md

------------------------------------------------------------------------

## 🧠 How the Flask App Base Works

### 🔧 App Factory

Handles app creation, environment selection, config loading, extension
initialization, blueprint registration, and logging.

### ⚙️ Configuration System

Supports layered configuration: 1. Base config\
2. Environment config\
3. Instance config\
4. External config (`YOURAPP_SETTINGS`)

Environment variables control secrets, DB URLs, debug mode, logging, and
more.

### 🧩 Extensions

Shared SQLAlchemy and Flask-Migrate instances live in `extensions.py`.

### 🌐 Blueprints

Routes organized by feature and registered in the app factory.

### 🚀 WSGI Entrypoint

`wsgi.py` loads the production app.

### 🧪 Testing Environment

Uses in-memory SQLite for clean test isolation.

------------------------------------------------------------------------

## 🔧 How to Configure Environments

### Development

Use `.env`:

    FLASK_ENV_NAME=development
    DEV_DATABASE_URL=sqlite:///dev.db
    FLASK_DEBUG=1
    SECRET_KEY=dev-secret

### Testing

Use `.env.test`:

    FLASK_ENV_NAME=testing
    TEST_DATABASE_URL=sqlite:///:memory:
    SECRET_KEY=test-secret

### Production

Environment variables:

    FLASK_ENV_NAME=production
    SECRET_KEY=your-secret
    DATABASE_URL=mysql://user:pass@host/db

### Instance Overrides

Store secrets in:

    instance/config.py

### External Config File

    export YOURAPP_SETTINGS=/path/to/file.cfg

------------------------------------------------------------------------

## 🌐 How to Add New Routes

Routes live in `routes.py`:

``` python
@main_bp.route("/about")
def about():
    return render_template("about.html")
```

JSON example:

``` python
@main_bp.route("/api/status")
def status():
    return {"status": "ok"}
```

------------------------------------------------------------------------

## 🎨 How to Add Templates and Static Files

### Templates

Place in:

    flaskapp/templates/

Extend `base.html`:

``` html
{% extends "base.html" %}
{% block content %}
<h1>About</h1>
{% endblock %}
```

### Static Files

Place in:

    flaskapp/static/

Reference:

``` html
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
```

------------------------------------------------------------------------

## 🧱 How to Scale the App Using Blueprints

### Create New Blueprint

    flaskapp/api/routes.py

``` python
api_bp = Blueprint("api", __name__, url_prefix="/api")
```

Register:

``` python
app.register_blueprint(api_bp)
```

------------------------------------------------------------------------

## 🗄️ How to Add Database Models

``` python
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
```

Use model:

``` python
db.session.add(Quote(text="Hello"))
db.session.commit()
```

------------------------------------------------------------------------

## 🛠️ How to Initialize the Database and Run Migrations

Initialize:

    flask db init

Migrate:

    flask db migrate -m "add quotes table"

Upgrade:

    flask db upgrade

------------------------------------------------------------------------

## 🧪 How to Test the App (Pytest + Fixtures + Database)

Fixtures:

``` python
@pytest.fixture()
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
```

Run tests:

    pytest
