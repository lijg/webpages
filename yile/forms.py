#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import InputRequired

class LoginForm(Form):
    name = TextField("name", validators=[InputRequired('Please enter your name.')])
    password = PasswordField('password', validators=[InputRequired('Please enter your password.')])
    remember_me = BooleanField('remember_me', default=False)
