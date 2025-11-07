from flask import Blueprint, render_template

# Create a blueprint. No url_prefix means it handles '/' at the root.
routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def home():
    # This will render templates/index.html
    return render_template('index.html')