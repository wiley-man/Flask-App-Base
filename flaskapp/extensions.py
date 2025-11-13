"""Extensions module for Flask application. 
This module initializes and configures extensions used in the app.
Currently, it sets up SQLAlchemy for database interactions 
and Flask-Migrate for handling database migrations.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()