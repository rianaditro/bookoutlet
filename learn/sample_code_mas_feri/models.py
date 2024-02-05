from ext import db

class Book(db.Model):
    __tablename__ = 'bookTable'

    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))