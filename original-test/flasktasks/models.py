from flask import request ,url_for
from datetime import datetime
from flask_login import  UserMixin
from flasktasks import db , login_manager
# import os
# from werkzeug import secure_filename

friends_table = db.Table('friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key = True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'),  primary_key = True)
)
requests_table = db.Table('request',
    db.Column('sender_id', db.Integer, db.ForeignKey('user.id' ),  primary_key = True),
    db.Column('reciever_id', db.Integer, db.ForeignKey('user.id'),  primary_key = True)
)
# User Table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')


    friends = db.relationship('User', 
                              secondary=friends_table,
                              primaryjoin=(friends_table.c.user_id == id),
                              secondaryjoin=(friends_table.c.friend_id == id) ,
                              backref=db.backref('friend_of', lazy='dynamic'),
                              lazy='dynamic')
    requests = db.relationship('User', 
                               secondary=requests_table,
                               primaryjoin=(requests_table.c.sender_id == id),
                               secondaryjoin=(requests_table.c.reciever_id == id),
                               backref=db.backref('requested_to', lazy='dynamic'),
                               lazy='dynamic')

    def __repr__(self):
        return f"(name: {self.name}, email: {self.email})"
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Tables = lowercase , Classes = Uppercase
    # notice we use 'user' to refrence a table's column,
    # and we used 'Post' to refrence a class
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # dunder/magic method for print user object
    def __repr__(self):
        return f"{self.title}, {self.content}, {self.date_posted}"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
