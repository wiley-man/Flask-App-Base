""" Module for defining routes and blueprint  in the Flask application. """
from flask import Blueprint, render_template
from sqlalchemy import func
from .models import *

# Define the main blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """ Route for the home page. """
    return "I'm the home page!"  # Placeholder response for home page