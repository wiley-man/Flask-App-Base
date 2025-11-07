import pytest
from flask import template_rendered
from dotenv import load_dotenv
from flaskapp import db, Quote


# If your package is named `yourapp` and exposes create_app in __init__.py:
from flaskapp import create_app
from tests.conftest import captured_templates

# overload the app fixture to pre-populate the database
@pytest.fixture(scope="session")
def app():
  load_dotenv(".env.test")
  app = create_app("testing")
  with app.app_context():
    db.create_all()
    db.session.add(Quote(text="Test quote", author="Tester"))
    db.session.commit()
    yield app
    db.session.remove()
    db.drop_all()


def test_home_status_and_content(client):
    """GET / returns 200 and expected content from the homepage template."""
    resp = client.get("/")
    assert resp.status_code == 200
    # Adjust the expected bytes below if your template text differs.
    assert b"Test quote" in resp.data


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
