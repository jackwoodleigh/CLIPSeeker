from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    db.Colmn(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True, default=func.now)) # uses current time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lowercase because stored lowercse in sql

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    notes = db.relationship('Note')