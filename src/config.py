from pathlib import Path

class BaseConfig:
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = "TheSecretKey"
    DEBUG = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = f"{BASE_DIR}/manage_db/uploaded"
    SQLALCHEMY_DATABASE_URI = "mysql://root:new-password@localhost:3306/book_db"
