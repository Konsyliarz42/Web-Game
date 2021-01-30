from datetime import date
from flask_restx import Api, Resource
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from . import make_response, render_template, request

from .forms import RegisterForm, LoginForm
from .models import db, User

api = Api()

def get_user():
    if current_user.is_authenticated:
        return {
            'id': current_user.id,
            'nick': current_user.nick,
            'email': current_user.email
        }

@api.route('/home')
class Home(Resource):

    def get(self):
        rform = RegisterForm()
        lform = LoginForm()

        if request.args.get('logout', True):
            logout_user()

        return make_response(render_template('home.html', user=get_user(), registerform=rform, loginform=lform), 200)


    def post(self):
        rform = RegisterForm()
        lform = LoginForm()
        code = 401

        # Register user
        if rform.validate_on_submit():
            user = User(
                email = rform.email.data,
                password = generate_password_hash(rform.password.data, 'sha256'),
                nick = rform.nick.data,
                created = date.today()
            )

            db.session.add(user)
            db.session.commit()

            user = User.query.filter_by(nick=rform.nick.data).first()
            login_user(user)
            rform = RegisterForm()
            code = 201

        # Login user
        if lform.validate_on_submit():
            user = User.query.filter_by(email=lform.email.data).first()
            login_user(user)
            rform = RegisterForm()
            code = 200

        return make_response(render_template('home.html', user=get_user(), registerform=rform, loginform=lform), code)