from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from random import randint

from .models_columns import TextPickleType
from .buildings.buildings import house

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    nick = db.Column(db.String(64), nullable=False)
    created = db.Column(db.Date, nullable=False)
    colonies = db.relationship('Colony')
    
    def __repr__(self):
        return f"<User: {self.nick}({self.email}) | id: {self.id}>"


class Colony(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.Date, nullable=False)
    position_x = db.Column(db.Integer, default=0)
    position_y = db.Column(db.Integer, default=0)
    resources = db.Column(TextPickleType())
    buildings = db.Column(TextPickleType())
    build_now = db.Column(TextPickleType())
    last_harvest = db.Column(db.DateTime, nullable=False)
    rapports = db.Column(TextPickleType(), default=dict())
    army = db.Column(TextPickleType(), default=dict())

    def __repr__(self):
        return f"<Colony: {self.name} | id: {self.id}>"


    def starter_pack(self):
        # Random position on map
        x = randint(0, 10)
        y = randint(0, 10)

        while Colony.query.filter_by(position_x=x, position_y=y).first():
            x = randint(0, 10)
            y = randint(0, 10)

        self.position_x = x
        self.position_y = y

        self.resources = {
            # name: [in magazine, production per hour]
            'wood': [1000, 0.0],
            'stone': [1000, 0.0],
            'food': [1000, 0.5],
            'gold': [100, 0.0]
        }

        self.buildings = {
            # name: {keys: values}
            'house': house(1)
        }