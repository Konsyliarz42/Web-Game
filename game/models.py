from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    nick = db.Column(db.String(64), nullable=False)
    created = db.Column(db.Date, nullable=False)
    colognes = db.relationship('Cologne')
    
    def __repr__(self):
        return f"<User: {nick}({email}) | id: {id}>"


class Cologne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Cologne: {name} | id: {id}>"