import os
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ADMIN_IDS = os.environ.get('ADMIN_IDS') or [1] # First user from database

class Config():
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or ('sqlite:///' + os.path.join(BASE_DIR, 'data.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or None


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id in ADMIN_IDS