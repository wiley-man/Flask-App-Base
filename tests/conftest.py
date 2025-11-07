import os
import pytest
from flaskapp import create_app
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