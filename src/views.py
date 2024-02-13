from flask import Blueprint, render_template
from flask import flash, request, redirect, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from extensions import db
from config import BaseConfig
from models import Book, User

import pandas, re, os


ALLOWED_EXTENSIONS = {'xlsx','xls'}

view = Blueprint("view",__name__)

@view.route("/")
def index():
    return redirect(url_for('view.catalog'))

def book_urls(books):
    urls = []
    for book in books.items:
        title = book.title
        to_url = re.sub(r'[^a-zA-Z0-9]+', '-', title.replace("-","")).lower()
        if to_url[-1] == "-":
            to_url = to_url[:-1]
            urls.append(to_url)
        else:
            urls.append(to_url)
    return urls

@view.route("/catalog",methods=["GET","POST"])
def catalog():
    page = request.args.get('page',1,type=int)
    per_page = 18

    if request.method == 'POST':
        search_query = request.form['search_query']
        books = Book.query.filter(Book.title.ilike(f"%{search_query}%")).paginate(page=page,per_page=per_page)
        book_url = book_urls(books)
        max_page = books.pages
        return render_template("catalog.html",books=books,urls=book_url,page=page,max_page=max_page, search_query=search_query)
    
    books = Book.query.paginate(page=page,per_page=per_page)
    book_url = book_urls(books)
    max_page = books.pages
    return render_template("catalog.html",books=books, urls = book_url,max_page=max_page,page=page)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@view.route("/upload",methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            messages = "no file"
            return redirect(url_for('view.table',messages=messages))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            messages = "no file"
            return redirect(url_for('view.table',messages=messages))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(BaseConfig.UPLOAD_FOLDER, filename))

            list_of_object = []
            df = pandas.read_excel(file)
            list_df = df.values.tolist()

            for l in list_df:
                dic = {
                    "title":f"{l[0]}",
                    "author":f"{l[1]}",
                    "price":f"{l[2]}",
                    "binding":f"{l[3]}",
                    "isbn":f"{l[4]}",
                    "publish_date":f"{l[5]}",
                    "publisher":f"{l[6]}",
                    "language":f"{l[7]}",
                    "page_count":f"{l[8]}",
                    "dimension":f"{l[9]}",
                    "image":f"{l[10]}"
                }
                list_of_object.append(dic)
                
            for obj in list_of_object:
                book = Book(title=obj['title'], 
                            author=obj['author'],
                            price=obj['price'],
                            binding=obj['binding'],
                            isbn=obj['isbn'],
                            publish_date=obj['publish_date'],
                            publisher=obj['publisher'],
                            language=obj['language'],
                            page_count=obj['page_count'],
                            dimension=obj['dimension'],
                            image=obj['image']
                            )
                try:
                    db.session.add(book)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
            return redirect(url_for("view.table"))
        else:
            messages = "no file"
            return redirect(url_for('view.table',messages=messages))
    return render_template('upload.html')

@view.route("/table",methods=["GET","POST"])
@login_required
def table():
    page = request.args.get('page',1,type=int)
    per_page = 18
    
    if request.form.get('search_query'):
        print(request.form.get('search_query'))
        search_query = request.form.get('search_query')
        books = Book.query.filter(Book.title.ilike(f"%{search_query}%")).paginate(page=page,per_page=per_page)
        max_page = books.pages
        return render_template("table.html",books=books,page=page,max_page=max_page, search_query=search_query)

    books = Book.query. paginate(page=page,per_page=per_page)
    max_page = books.pages
    return render_template("table.html",books=books,max_page=max_page,page=page)

@view.route("/add",methods=["GET","POST"])
@login_required
def add():
    if request.form:
        data = request.form
        item = Book(title=data.get("title"),
                isbn=data.get("isbn"),
                author=data.get("author"),
                price=data.get("price"),
                binding=data.get("binding"),
                publish_date=data.get("publish_date"),
                publisher=data.get("publisher"),
                language=data.get("language"),
                page_count=data.get("page_count"),
                dimension=data.get("dimension"),
                image=data.get("image"))
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('view.table'))
    return render_template('form.html')

@view.route("/edit",methods=["GET","POST"])
@login_required
def edit():
    isbn = request.args.get('isbn')
    books = Book.query.get(isbn)
    if request.form:
        data = request.form
        isbn = data.get('isbn')
        books = Book.query.get(isbn) #object Book

        books.title = data.get('title')
        books.author = data.get('author')
        books.price = data.get('price')
        books.binding = data.get('binding')
        books.publish_date = data.get('publish_date')
        books.publisher = data.get('publisher')
        books.language = data.get('language')
        books.page_count = data.get('page_count')
        books.dimension = data.get('dimension')
        books.image = data.get('image')

        db.session.commit()
        return redirect(url_for('view.table'))
        
    return render_template('form.html',data=books)

@view.route("/delete",methods=["GET","POST"])
@login_required
def delete():
    isbn = request.args.get('isbn')
    books = Book.query.get(int(isbn))
    try:
        db.session.delete(books)
        db.session.commit()
    except AttributeError:
        flash("No data selected")
        return redirect(url_for('view.table'))

    return redirect(url_for('view.table'))

