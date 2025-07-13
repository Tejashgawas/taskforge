from . import db
from datetime import datetime

class Article(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    content = db.Column(db.String(100),nullable = False)
    created_at = db.Column(db.DateTime,default = datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # plain for now (add hashing later)
