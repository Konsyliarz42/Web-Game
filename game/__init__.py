import os
from flask import Flask, make_response, render_template
from config import Config
from . import routes

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
app.config.from_pyfile(os.path.join(app.instance_path, 'config.py'), silent=True)

routes.api.init_app(app)