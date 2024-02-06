from .extensions import db


class Book(db.Model):
    __tablename__ = "bookTable"
    index = db.Column(db.Float(), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author=db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    binding=db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.Integer(), primary_key=True)
    publisher_date = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(255), nullable=False)
    page_count = db.Column(db.Integer(), nullable=False)
    dimension = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)