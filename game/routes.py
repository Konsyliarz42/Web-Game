from flask_restx import Api, Resource 
from . import make_response, render_template

from .forms import LoginForm

api = Api()

@api.route('/home')
class Home(Resource):

    def get(self):
        info = None
        form = LoginForm()

        return make_response(render_template('home.html', info=info, form=form), 200)


    def post(self):
        info = None
        form = LoginForm()

        if form.validate_on_submit():
            return make_response("Good", 200)

        return make_response(render_template('home.html', info=info, form=form), 401)