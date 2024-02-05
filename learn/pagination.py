from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bookoutlet.sqlite"
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'bookTable'

    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
db.create_all()

@app.route("/")
def index():
    page = request.args.get('page',1,type=int)
    per_page = 10
    records = Book.query.paginate(page=page,per_page=per_page,error_out=False)

    return render_template(template_name_or_list='index.html',
                           records=records)

if __name__=="__main__":
    app.run(debug=True)