# Flask Application Base

**Here’s a clean, battle-tested way to configure a Flask app for development, testing, and production using the app-factory pattern, config classes, and environment variables.**

## 1) Project layout

```bash
yourapp/
├─ yourapp/
│  ├─ __init__.py        # app factory lives here
│  ├─ routes.py
│  ├─ models.py
│  └─ config.py          # all configs in one place
├─ instance/             # machine-specific, not committed
│  └─ config.py          # optional local secrets/overrides
├─ .env                  # dev-only env vars (never in prod)
├─ .env.test             # test-only env vars
├─ wsgi.py               # for prod servers (gunicorn/uwsgi)
└─ tests/
├─ conftest.py
└─ test_example.py
```

## 2) Config classes (yourapp/config.py)

```python
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB = f"sqlite:///{os.path.join(BASE_DIR, '..', 'app.db')}"

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure")  # override in prod!
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", DEFAULT_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    # Logging level (can be overridden)
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

class DevelopmentConfig(Config):
    DEBUG = True
    # Helpful for dev: show Werkzeug debugger, etc.
    # Use a separate dev DB if you like
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL", DEFAULT_DB)

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    # In-memory DB by default for isolation/speed
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "sqlite:///:memory:")
    WTF_CSRF_ENABLED = False  # usually disabled for tests
    # Make cookies non-secure to avoid HTTPS requirement in tests
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    # Production must provide strong secrets + real DB
    SECRET_KEY = os.environ["SECRET_KEY"]      # crash early if missing
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    # Example: stricter headers
    # SEND_FILE_MAX_AGE_DEFAULT = 31536000
```

## 3) App factory (yourapp/__init__.py)

```python
import logging
import os
from flask import Flask
from .config import DevelopmentConfig, TestingConfig, ProductionConfig
from .routes import bp as routes_bp  # assume you have a blueprint

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

def create_app(config_name: str | None = None) -> Flask:
    # Allow env var to choose config (default: development)
    config_name = config_name or os.getenv("FLASK_ENV_NAME", "development")

    app = Flask(__name__, instance_relative_config=True)

    # Base config from class
    app.config.from_object(CONFIG_MAP[config_name])

    # Optional: load instance/ config (ignored if missing)
    app.config.from_pyfile("config.py", silent=True)

    # Optional: allow an env var to point to a file with secrets
    # e.g., export YOURAPP_SETTINGS=/path/to/production.cfg
    app.config.from_envvar("YOURAPP_SETTINGS", silent=True)

    # Blueprints, extensions, CLI, etc.
    app.register_blueprint(routes_bp)

    _configure_logging(app)

    return app

def _configure_logging(app: Flask) -> None:
    # Simple per-environment logging
    level = getattr(logging, app.config.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    fmt = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    app.logger.setLevel(level)
    if not any(isinstance(h, logging.StreamHandler) for h in app.logger.handlers):
        app.logger.addHandler(handler)
```

Why FLASK_ENV_NAME?

Flask 3.x removed FLASK_ENV. You control debug mode with FLASK_DEBUG=1, and you choose your config class yourself (here via 

FLASK_ENV_NAME=development|testing|production).

## 4) Environment selection

### Development (local)

.env (auto-loaded by flask run via python-dotenv):

```ini
FLASK_APP=wsgi.py
FLASK_DEBUG=1
FLASK_ENV_NAME=development
DEV_DATABASE_URL=sqlite:///dev.db
SECRET_KEY=dev-only
```

Run:

```bash
flask run
```

or

```bash
python -m flask run
```

### Testing (pytest)

.env.test (loaded in tests if you call dotenv.load_dotenv('.env.test')):

```ini
FLASK_ENV_NAME=testing
TEST_DATABASE_URL=sqlite:///:memory:
```

tests/conftest.py:

```python
import os
import pytest
from yourapp import create_app
from dotenv import load_dotenv

@pytest.fixture(scope="session")
def app():
  load_dotenv(".env.test")
  app = create_app("testing")
  with app.app_context():
      yield app

@pytest.fixture()
def client(app):
  return app.test_client()
```

### Production

Set real environment variables at deploy time (no .env files):

```ini
export FLASK_ENV_NAME=production
export SECRET_KEY='super-long-random-string'
export DATABASE_URL='postgresql+psycopg://user:pass@host/db'
export LOG_LEVEL=INFO
```

WSGI entry (wsgi.py):

```python
from yourapp import create_app
app = create_app()  # picks up FLASK_ENV_NAME
```

Example gunicorn command:

```bash
gunicorn "wsgi:app" --bind 0.0.0.0:8000 --workers 3
```

## 5) Instance config (optional)

Anything in instance/config.py is ignored by git and loads after your class config—great for per-host overrides:

\# instance/config.py

```ini
SECRET_KEY = "dev-machine-secret"
```

## 6) Common gotchas & tips

- **Secrets:** never commit real SECRET_KEY or credentials. In prod, force them via os.environ["..."] to fail fast if missing.

- **Debug vs. Config:** FLASK_DEBUG=1 toggles debugger/reloader; it does not choose your database or other settings—your config class does.

- **Testing DB:** use sqlite:///:memory: or a throwaway Postgres DB per test session; create/drop schema in fixtures as needed.

- **Overrides order (later wins):**

1. Config class
2. instance/config.py
3. YOURAPP_SETTINGS file
4. app.config.from_mapping(...) if you add it

- **Logging:** tune per env (e.g., JSON logs in prod, DEBUG in dev).

- **Extensions:** initialize inside create_app so they respect the chosen config.
