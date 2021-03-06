from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from datetime import date, datetime

from game import app
from game.models import db, User, Colony

MAIN_TESTER = {
    'email': "tester@game.com",
    'password': 'testPassword',
    'nick': "Tester",
    'colony_name': "TesterColony"
}

class MyTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['LOGIN_DISABLED'] = True
        return app

    
    def setUp(self):
        db.create_all()

        # Add tester
        db.session.add(User(
            email = MAIN_TESTER['email'],
            password = generate_password_hash(MAIN_TESTER['password'], 'sha256'),
            nick = MAIN_TESTER['nick'],
            created = date.today()
        ))

        # Add tester's colony
        colony = Colony(
            name = MAIN_TESTER['colony_name'],
            owner = 1,
            created = date.today(),
            build_now = dict(),
            last_harvest = datetime.now()
        )
        colony.starter_pack()
        db.session.add(colony)

        db.session.commit()

    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
