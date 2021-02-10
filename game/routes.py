from datetime import date, timedelta
from flask_restx import Api, Resource
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from . import make_response, render_template, request, redirect, url_for

from .routes_functions import get_user, get_colonies, translate_keys, get_next_buildings
from .forms import RegisterForm, LoginForm, NewColonyForm
from .models import db, User, Colony

from datetime import timedelta

api = Api()

@api.route('/home')
class Home(Resource):

    def get(self):
        rform = RegisterForm()
        lform = LoginForm()

        # Logout user
        if bool(request.args.get('logout')) == True:
            logout_user()

        return make_response(render_template('home.html',
            user=get_user(),
            registerform=rform,
            loginform=lform,
        ), 200)


    def post(self):
        rform = RegisterForm()
        lform = LoginForm()

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
            return make_response(redirect(url_for('game')), 301) 

        # Login user
        if lform.validate_on_submit():
            user = User.query.filter_by(email=lform.email.data).first()
            login_user(user)
            return make_response(redirect(url_for('game')), 301) 

        return make_response(render_template('home.html',
            user=get_user(),
            registerform=rform,
            loginform=lform
        ), 401)


@login_required
@api.route('/game')
class Game(Resource):

    def get(self):
        cform = NewColonyForm()

        return make_response(render_template('game.html',
            user=get_user(),
            colonies=get_colonies(),
            colonyform=cform
        ), 200)

    
    def post(self):
        cform = NewColonyForm()
        code = 401

        # Create colony
        if cform.validate_on_submit():
            colony = Colony(
                name = cform.name.data,
                owner = current_user.id,
                created = date.today()
            )

            colony.starter_pack()
            db.session.add(colony)
            db.session.commit()

            cform = NewColonyForm()
            code = 201

        return make_response(render_template('game.html',
            user=get_user(),
            colonies=get_colonies(),
            colonyform=cform
        ), code)


@login_required
@api.route('/game/colonies/<int:colony_id>')
class ColonyPage(Resource):

    def get(self, colony_id):
        colony = Colony.query.filter_by(id=colony_id, owner=current_user.id).first()

        if not colony:
            return make_response("You not have permission to view this page!", 401)

        colony = {
            'id': colony.id,
            'owner': current_user.nick,
            'name': colony.name,
            'created': colony.created,
            'created_days': (date.today() - colony.created).days,

            'position': {
                'x': colony.position_x,
                'y': colony.position_y
            },

            'main_resources': translate_keys(colony.resources),
            'buildings': translate_keys(colony.buildings)
        }

        return make_response(render_template('colony.html',
            user=get_user(),
            colony=colony
        ), 200)


@login_required
@api.route('/game/colonies/<int:colony_id>/build')
class ColonyBuild(Resource):

    def get(self, colony_id):
        colony = Colony.query.filter_by(id=colony_id, owner=current_user.id).first()

        if not colony:
            return make_response("You not have permission to view this page!", 401)

        buildings = translate_keys(get_next_buildings(colony.buildings))

        colony = {
            'id': colony.id,
            'owner': current_user.nick,
            'name': colony.name,
            'created': colony.created,
            'created_days': (date.today() - colony.created).days,

            'position': {
                'x': colony.position_x,
                'y': colony.position_y
            },

            'main_resources': translate_keys(colony.resources),
        }

        return make_response(render_template('colony_build.html',
            user=get_user(),
            colony=colony,
            buildings=buildings
        ), 200)