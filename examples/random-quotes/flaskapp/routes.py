# yourapp/routes.py
from flask import Blueprint, render_template
from sqlalchemy import func
from .models import Quote

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/")
def home():
    row = Quote.query.order_by(func.random()).first()
    if row is None:
        quote, author = "No quotes yet. Run: flask db upgrade && flask seed-quotes", None
    else:
        quote, author = row.text, (row.author or None)
    return render_template("index.html", quote=quote, author=author)

@routes_bp.route("/about")
def about():
    return render_template("about.html")
