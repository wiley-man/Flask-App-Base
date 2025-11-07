# tests/test_home.py
import pytest
from flask import template_rendered
from contextlib import contextmanager

# If your package is named `yourapp` and exposes create_app in __init__.py:
from flaskapp import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


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


def test_home_status_and_content(client):
    """GET / returns 200 and expected content from the homepage template."""
    resp = client.get("/")
    assert resp.status_code == 200
    # Adjust the expected bytes below if your template text differs.
    assert b"Hello from the Flask home page" in resp.data


def test_home_uses_index_template(app, client):
    """The home view renders index.html."""
    with captured_templates(app) as templates:
        _ = client.get("/")
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == "index.html"


def test_home_route_is_registered(app):
    """The blueprint is mounted at root with '/' -> endpoint 'routes.home'."""
    # The endpoint name is <blueprint_name>.<view_func_name>
    endpoints = {(r.rule, r.endpoint) for r in app.url_map.iter_rules()}
    assert ("/", "routes.home") in endpoints
