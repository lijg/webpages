#!/usr/bin/python
# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    index = db.Column(db.Integer)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))

    def __unicode__(self):
        return self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(512), unique=True)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
    
    def __repr__(self):
        """
        Returns name
        """
        return '<User %r>' % self.name

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    """
    Flask-Login expects methods.
    """
    def is_active(self):
        """
        Returns `True`.
        """
        return True
    
    def is_authenticated(self):
        """
        Returns `True`.
        """
        return True
    
    def is_anonymous(self):
        """
        Returns `False`.
        """
        return False
    
    def get_id(self):
        """
        Assuming that the user object has an `id` attribute, this will take
        that and convert it to `unicode`.
        """
        return unicode(self.id)

