from flask_login import UserMixin
from . import db

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(100), unique=True)
    password = db.Column(db.Text(100), unique=False)
    balance = db.Column(db.Text(100), unique=False)
    accountType = db.Column(db.Text(100), unique=False)


class Bars(UserMixin,db.Model):
    __tablename__ = "bars"
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    username = db.Column(db.Text(100), unique=True)
    password = db.Column(db.Text(100), unique=False)
    name = db.Column(db.Text(100), unique=False)
    accountType = db.Column(db.Text(100), unique=False)




