from pathlib import Path

class BaseConfig:
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = "TheSecretKey"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = f"{BASE_DIR}/manage_db/uploaded"
    SQLALCHEMY_DATABASE_URI = "sqlite:///old.sqlite"
    DEBUG = True
