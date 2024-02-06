from flask import request,redirect,render_template,flash,url_for
from werkzeug.utils import secure_filename
from pathlib import Path

from manage_db.convert import BookExcel, excel_to_object


ALLOWED_EXTENSIONS = {"xls","xlsx"}
BASE_DIR = Path(__file__).resolve().parent

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower()    

def upload_excel():
    pass

