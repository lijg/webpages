#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    index = db.Column(db.Integer)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))

    def __unicode__(self):
    	return self.name
