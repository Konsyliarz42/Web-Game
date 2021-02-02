from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin

from .models_columns import TextPickleType

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    nick = db.Column(db.String(64), nullable=False)
    created = db.Column(db.Date, nullable=False)
    colonies = db.relationship('Colony')
    
    def __repr__(self):
        return f"<User: {self.nick}({self.email}) | id: {id}>"


class Colony(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.Date, nullable=False)

    position_x = db.Column(db.Integer, default=0)
    position_y = db.Column(db.Integer, default=0)

    rescuers = db.Column(TextPickleType())
    buildings = db.Column(TextPickleType())

    def __repr__(self):
        return f"<Colony: {self.name} | id: {self.id}>"


    def starter_pack(self):
        self.rescuers = {
            # name: [in magazine, production per hour]
            'gold': [100, 0.0],
            'wood': [500, 0.0],
            'stone': [500, 0.0],
            'clay': [250, 0.0],
            'food': [1000, 0.5],
        }

        self.buildings = {
            
        }