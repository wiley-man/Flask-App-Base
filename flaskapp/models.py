from .extensions import db

class Quote(db.Model):
    __tablename__ = "quotes"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255))

    def __repr__(self):
        return f"<Quote id={self.id} author={self.author} text={self.text[:60]}...>"