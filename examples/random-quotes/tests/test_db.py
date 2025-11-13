from flaskapp import Quote, db
import pytest

def test_db_is_empty(session):
    """Database starts empty."""
    count = session.query(Quote).count()
    assert count == 0

def test_add_quote(session):
    """Can insert a quote into the database."""
    q = Quote(text="Testing is essential.", author="QA Bot")
    session.add(q)
    session.commit()

    stored = Quote.query.first()
    assert stored is not None
    assert stored.text == "Testing is essential."
    assert stored.author == "QA Bot"

def test_multiple_quotes_and_random(session):
    """Can store multiple quotes and select randomly."""
    quotes = [
        Quote(text="One", author="A"),
        Quote(text="Two", author="B"),
        Quote(text="Three", author="C"),
    ]
    session.add_all(quotes)
    session.commit()

    all_quotes = Quote.query.all()
    assert len(all_quotes) == 4  # 1 from test_add_quote + 3 new

    # Using SQLAlchemy func.random() to simulate random selection
    from sqlalchemy import func
    random_quote = Quote.query.order_by(func.random()).first()
    assert isinstance(random_quote, Quote)
    assert random_quote.text in {q.text for q in all_quotes}