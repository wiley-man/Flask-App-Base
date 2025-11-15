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
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]  # crash early if missing
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    # Example: stricter headers
    # SEND_FILE_MAX_AGE_DEFAULT = 31536000