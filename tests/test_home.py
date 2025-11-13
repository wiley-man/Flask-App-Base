import pytest
from .conftest import client


def test_home_status_and_content(client):
    """GET / returns 200 and expected content from the homepage template."""
    resp = client.get("/")
    assert resp.status_code == 200
    # Adjust the expected bytes below if your template text differs.
    assert b"I'm the home page!" in resp.data
