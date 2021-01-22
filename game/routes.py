from flask_restx import Api, Resource 
from . import make_response, render_template

api = Api()

@api.route('/home')
class Home(Resource):

    def get(self):
        return make_response(render_template('home.html'), 200)