import logging
import os
import csv
from flask import Flask
from .config import DevelopmentConfig, TestingConfig, ProductionConfig
from .routes import routes_bp # assume you have a blueprint
from .extensions import db, migrate
from .models import Quote

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

def create_app(config_name: str | None = None) -> Flask:
    # Allow env var to choose config (default: development)
    config_name = config_name or os.getenv("FLASK_ENV_NAME", "development")

    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Base config from class
    app.config.from_object(CONFIG_MAP[config_name])

    # Optional: load instance/ config (ignored if missing)
    app.config.from_pyfile("config.py", silent=True)

    # Optional: allow an env var to point to a file with secrets
    # e.g., export YOURAPP_SETTINGS=/path/to/production.cfg
    app.config.from_envvar("YOURAPP_SETTINGS", silent=True)

    # ---- Extensions ----
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints, extensions, CLI, etc.
    app.register_blueprint(routes_bp)

    _configure_logging(app)

    # LOGGING EXAMPLE
    app.logger.info(f"Starting app in {config_name} mode")
    
    # ---- CLI: seed data ----
    @app.cli.command("seed-quotes")
    def seed_quotes():
        """Insert a few sample quotes (idempotent-ish)."""

        # Load sample seed data from CSV
        SEED_DATA_FILE = os.environ.get("SEED_DATA_FILE")
        if SEED_DATA_FILE and Quote.query.count() == 0:
            # Using DictReader (for header-based access)
            with open(SEED_DATA_FILE, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                samples = []
                for row in reader:
                    quote = Quote(id=row['id'], text=row['text'], author=row['author'])
                    samples.append(quote)
                    print(f"Prepared Quote({quote})")

                # Only add if table is empty
                db.session.add_all(samples)
                db.session.commit()
                print("Seeded sample quotes.")
        else:
            print("Quotes already present or not configured; skipping seed.")

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

