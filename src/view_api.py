from flask import Blueprint,request,jsonify
from models import Book

import json,math


api = Blueprint("api",__name__)

@api.route("/api/book")
def main():
    page = request.args.get("page",1,type=int)
    per_page = 18
    template_return = dict()
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
            "image":book.image}
        book_in_page.append(item)
        template_return["result"] = book_in_page
    return jsonify(template_return)

