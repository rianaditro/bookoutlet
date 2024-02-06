import os
from pathlib import Path

class BaseConfig:
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = "TheSecretKey"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER  = os.path.join(BASE_DIR, 'media')
