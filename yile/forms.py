#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, TextField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Required, Length, Regexp, EqualTo, Email
from models import User

class LoginForm(Form):
    name = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('password', validators=[InputRequired('Please enter your password.')])
    remember_me = BooleanField('remember_me', default=False)

class RegistrationForm(Form):
    name = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password_confirm', message='Passwords must match.')])
    password_confirm = PasswordField('Confirm password', validators=[Required()])

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')
