from sqlalchemy.orm import Mapped, mapped_column

from .extensions import db


class Book(db.Model):
    __tablename__ = "bookTable"
    title:Mapped[str]
    author:Mapped[str]
    price:Mapped[float]
    binding:Mapped[str]
    isbn:Mapped[int] = mapped_column(primary_key=True)
    publisher_date = Mapped[str]
    publisher = Mapped[str]
    language = Mapped[str]
    page_count = Mapped[int]
    dimension = Mapped[str]
    image = Mapped[str]