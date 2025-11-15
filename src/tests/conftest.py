import os
from dotenv import load_dotenv
import pytest
from flaskapp import create_app, db
from flask.signals  import template_rendered
from contextlib import contextmanager

@pytest.fixture(scope="session")
def app():
  load_dotenv(".env.test")
  app = create_app("testing")
  with app.app_context():
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()

@pytest.fixture()
def client(app):
  return app.test_client()

@pytest.fixture()
def session(app):
    """Provide a fresh database session for each test."""
    with app.app_context():
        yield db.session
        db.session.rollback()

@contextmanager
def captured_templates(app):
    """Capture which templates were rendered during a request."""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)