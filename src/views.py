from flask import Blueprint, render_template
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from extensions import db
from models import Book

import pandas


ALLOWED_EXTENSIONS = {'xlsx','xls'}


view = Blueprint("view",__name__)


@view.route("/homepage")
def index():
    return render_template("index.html")

@view.route("/catalog",methods=["GET","POST"])
def catalog():
    page = request.args.get('page',1,type=int)
    per_page = 18

    if request.method == 'POST':
        search_query = request.form['search_query']
        books = Book.query.filter(Book.title.ilike(f"%{search_query}%")).paginate(page=page,per_page=per_page)
        max_page = books.pages
        return render_template("catalog.html",books=books,page=page,max_page=max_page, search_query=search_query)
    
    books = Book.query.paginate(page=page,per_page=per_page)
    max_page = books.pages
    return render_template("catalog.html",books=books,max_page=max_page,page=page)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@view.route("/upload",methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('download_file', name=filename))

        list_of_object = []
        df = pandas.read_excel(file)
        list_df = df.values.tolist()

        for l in list_df:
            dic = {
                "title":l[0],
                "author":l[1],
                "price":l[2],
                "binding":l[3],
                "isbn":l[4],
                "publish_date":l[5],
                "publisher":l[6],
                "language":l[7],
                "page_count":l[8],
                "dimension":l[9],
                "image":l[10]
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
            
            db.session.add(book)
            db.session.commit()
        return redirect(url_for("view.table"))
    return render_template("upload.html")

@view.route("/table",methods=["GET","POST"])
def table():
    page = request.args.get('page',1,type=int)
    per_page = 18
    
    if request.method == 'POST':
        
        # if bool(request.form['search_query']):
        #     print(request.form['search_query'])
        #     search_query = request.form['search_query']
        #     books = Book.query.filter(Book.title.ilike(f"%{search_query}%")).paginate(page=page,per_page=per_page)
        #     max_page = books.pages
        #     return render_template("table.html",books=books,page=page,max_page=max_page, search_query=search_query)
        # else:
            books = Book.query.paginate(page=page,per_page=per_page)
            max_page = books.pages
            return render_template("table.html",books=books,max_page=max_page,page=page)
    
    books = Book.query.paginate(page=page,per_page=per_page)
    max_page = books.pages
    return render_template("table.html",books=books,max_page=max_page,page=page)

@view.route("/add",methods=["GET","POST"])
def add():
    if request.form:
        data = request.form
        item = Book(title=data.get("title"),
                isbn=data.get("isbn"),
                author="author",
                price="123",
                binding="binding",
                publish_date="publish date",
                publisher="publsiher",
                language="language",
                page_count="page count",
                dimension="dimension",
                image="image")
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('view.table'))
    return render_template('form.html')

@view.route("/edit",methods=["GET","POST"])
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