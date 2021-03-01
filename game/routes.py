from datetime import date, timedelta
from flask_restx import Api, Resource
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from . import make_response, render_template, request, redirect, url_for

from .routes_functions import get_user, get_colonies, translate_keys, get_next_buildings, update_colony, get_map
from .forms import RegisterForm, LoginForm, NewColonyForm
from .models import db, User, Colony

from datetime import timedelta, datetime

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
        print(request.form, bool(request.form['register']), bool(request.form['login']))

        # Register user
        if bool(request.form['register']):
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
        elif bool(request.form['login']):
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
                created = date.today(),
                build_now = dict(),
                last_harvest = datetime.now()
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

        messages = update_colony(colony_id)
        colony = get_colonies(colony_id)

        if not colony:
            return make_response("You not have permission to view this page!", 401)

        colony_db = Colony.query.filter_by(id=colony_id).first()
        build = [key for key in translate_keys(colony_db.build_now)]
        
        return make_response(render_template('colony.html',
            user=get_user(),
            messages=translate_keys(messages),
            colony=translate_keys(colony),
            build_list=build
        ), 200)


@login_required
@api.route('/game/colonies/<int:colony_id>/build')
class ColonyBuild(Resource):

    def get(self, colony_id):

        messages = update_colony(colony_id)
        colony = get_colonies(colony_id)
        

        if not colony:
            return make_response("You not have permission to view this page!", 401)

        colony_db = Colony.query.filter_by(id=colony_id).first()
        build = [key for key in translate_keys(colony_db.build_now)]
        buildings = get_next_buildings(colony_db.buildings, colony_db.resources, colony_db.build_now)

        return make_response(render_template('colony_build.html',
            user=get_user(),
            colony=translate_keys(colony),
            messages=translate_keys(messages),
            buildings=translate_keys(buildings),
            build_list=build
        ), 200)


    def post(self, colony_id):

        colony = Colony.query.filter_by(id=colony_id).first()
        buildings = get_next_buildings(colony.buildings, colony.resources, colony.build_now)

        # Remove building from build_now
        if request.form.get('cannel'):
            build = request.form['cannel']
            queue = [key for key in colony.build_now.keys()]
            colony.build_now.pop(build)

            # Update time in other buildings
            if colony.build_now:
                buildings_timedelta = timedelta()

                for building in colony.build_now.keys():
                    b = colony.build_now[building]['build_time_dict']
                    bt = timedelta(
                        days=b['days'],
                        hours=b['hours'],
                        minutes=b['minutes'],
                        seconds=b['seconds']
                    )

                    # Pass the building which was first in queue before remove
                    if queue[0] != building:
                        colony.build_now[building]['build_start'] = datetime.now() + buildings_timedelta
                        colony.build_now[building]['build_end'] = colony.build_now[building]['build_start'] + bt

                    buildings_timedelta += bt

        # Add building to build_now
        if request.form.get('build'):
            build = buildings[request.form['build']]

            # Subtraction build cost form colony resources
            for resource in build['build_cost']:
                colony.resources[resource][0] -= build['build_cost'][resource]

            # Add building to build list
            build['build_start'] = datetime.now()
            build['build_end'] = build['build_time']

            for building in colony.build_now:
                build['build_start'] = colony.build_now[building]['build_end']
                build['build_end'] += build['build_time']

            build['build_end'] += datetime.now()
            colony.build_now.update({request.form['build']: build})

        # Save changes
        Colony.query.filter_by(id=colony_id).update({
            'resources': colony.resources,
            'build_now': colony.build_now
        })
        db.session.commit()

        return make_response(
            redirect(url_for('colony_build', colony_id=colony_id)
        ), 303)


@login_required
@api.route('/game/colonies/<int:colony_id>/production')
class ColonyProduction(Resource):

    def get(self, colony_id):

        messages = update_colony(colony_id)
        colony = get_colonies(colony_id)

        if not colony:
            return make_response("You not have permission to view this page!", 401)

        colony_db = Colony.query.filter_by(id=colony_id).first()
        build = [key for key in translate_keys(colony_db.build_now)]
        production = dict()
        buildings = dict()

        for res in colony_db.resources:
            production[res] = colony_db.resources[res][1]
            
        for bui in colony_db.buildings:
            buildings[bui] = dict()

            for res in colony_db.resources:
                if res in colony_db.buildings[bui]['production']:
                    buildings[bui][res] = colony_db.buildings[bui]['production'][res]
                else:
                    buildings[bui][res] = 0

            buildings[colony_db.buildings[bui]['name']] = buildings[bui]
            buildings.pop(bui)
            
        return make_response(render_template('colony_production.html',
            user=get_user(),
            colony=translate_keys(colony),
            messages=translate_keys(messages),
            build_list=build,
            production=translate_keys(production),
            buildings=translate_keys(buildings)
        ), 200)


@login_required
@api.route('/game/colonies/<int:colony_id>/map')
class ColonyMap(Resource):

    def get(self, colony_id):
        messages = update_colony(colony_id)
        colony = get_colonies(colony_id)

        if not colony:
            return make_response("You not have permission to view this page!", 401)

        colony_db = Colony.query.filter_by(id=colony_id).first()
        build = [key for key in translate_keys(colony_db.build_now)]
        positions = get_map()

        return make_response(render_template('colony_map.html',
            user=get_user(),
            colony=translate_keys(colony),
            messages=translate_keys(messages),
            build_list=build,
            position=positions
        ), 200)