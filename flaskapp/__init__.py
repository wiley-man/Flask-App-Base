import logging
import os
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

    # ---- CLI: seed data ----
    @app.cli.command("seed-quotes")
    def seed_quotes():
        """Insert a few sample quotes (idempotent-ish)."""
        samples = [
            Quote(text="Simplicity is the soul of efficiency", author="Austin Freeman"),
            Quote(text="Programs must be written for people to read", author="Harold Abelson"),
            Quote(text="Talk is cheap. Show me the code", author="Linus Torvalds"),
            Quote(text="Any sufficiently advanced technology is indistinguishable from magic", author="Arthur C. Clarke"),
            Quote(text="The best way to predict the future is to invent it", author="Alan Kay"),
            Quote(text="Stay hungry, stay foolish.", author="Steve Jobs"),
            Quote(text="Growth and comfort do not coexist", author="Ginni Rommetty"),
            Quote(text="Technology is best when it brings people together", author="Matt Mullenweg"),
            Quote(text="The technology you use impresses no one. The experience you create with it is everything", author="Sean Gerety"),
            Quote(text="The advance of technology is based on making it fit in so that you don’t really even notice it, so it’s part of everyday life.", author="Bill Gates"),
            Quote(text="If you’re offered a seat on a rocket ship, don’t ask what seat.", author="Sheryl Sandberg"),
            Quote(text="You can focus on things that are barriers or you can focus on scaling the wall or redefining the problem", author="Tim Cook"),
            Quote(text="Don’t be afraid to change the model", author="Reed Hastings"),
            Quote(text="Never trust a computer you can’t throw out a window", author="Steven Wozniak"),
            Quote(text="Never let a computer know you’re in a hurry", author="author unknown"),
            Quote(text="Hardware: The parts of a computer system that can be kicked", author="Jeff Pesis"),
            Quote(text="Once a new technology rolls over you, if you’re not part of the steamroller, you’re part of the road.", author="Stewart Brand"),
            Quote(text="If it keeps up, man will atrophy all his limbs but the push-button finger.", author="Frank Lloyd Wright"),
            Quote(text="Technology is ruled by two types of people: those who manage what they do not understand, and those who understand what they do not manage.", author="Make Trout"),
            Quote(text="Technology is like a fish. The longer it stays on the shelf, the less desirable it becomes.", author="Andrew Heller"),
            Quote(text="I just invent. Then I wait until man comes around to needing what I’ve invented", author="R. Buckminster Fuller"),
            Quote(text="Computers have lots of memory but no imagination", author="author unknown"),
            Quote(text="People who smile while they are alone used to be called insane until we invented smartphones and social media", author="Mokokoma Mokhonoana"),
            Quote(text="I won’t be impressed with technology until I can download food", author="author unknown"),
            Quote(text="Life was much easier when Apple and Blackberry were just fruits", author="author unknown"),
        ]
        # Only add if table is empty
        if Quote.query.count() == 0:
            db.session.add_all(samples)
            db.session.commit()
            print("Seeded sample quotes.")
        else:
            print("Quotes already present; skipping seed.")

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

