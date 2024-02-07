from flask import Blueprint,request,jsonify
from models import Book

import json,math


api = Blueprint("api",__name__)

@api.route("/api")
def main():
    per_page = 18
    max_books = len(Book.query.all())
    max_page = math.ceil(max_books/per_page)
    template_retun = dict()
    for page in range(1,max_page+1):
        books = Book.query.paginate(page=page,per_page=per_page)
        book_in_page = []
        for book in books:
            item = {
                "title":book.title,
                "author":book.author,
                "price":book.price,
                "binding":book.binding,
                "isbn":book.isbn,
                "publish_date":book.publish_date,
                "publisher":book.publisher,
                "language":book.language,
                "page_count":book.page_count,
                "dimension":book.dimension,
                "image":book.image
            }
            book_in_page.append(item)
        template_retun[page] = book_in_page
    return jsonify(template_retun)

