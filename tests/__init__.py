from flask_testing import TestCase

from game import app
from game.models import db, User, Colony

class MyTestCase(TestCase):
    def create_app(self):

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['LOGIN_DISABLED'] = True
        return app

    
    def setUp(self):

        db.create_all()

    
    def tearDown(self):

        db.session.remove()
        db.drop_all()