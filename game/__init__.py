import os
from flask import Flask, make_response, render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from . import routes, models
from config import Config, AdminModelView

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
app.config.from_pyfile(os.path.join(app.instance_path, 'config.py'), silent=True)

routes.api.init_app(app)

models.db.init_app(app)
models.db.create_all(app=app)

login_manager = LoginManager()
login_manager.init_app(app)

admin = Admin(app)
admin.add_view(AdminModelView(models.User, models.db.session))
admin.add_view(AdminModelView(models.Colony, models.db.session))

Bootstrap(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)