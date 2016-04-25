#!/usr/bin/python
# -*- coding: utf-8 -*-
import imghdr
from flask import flash
from flask_wtf import Form
from wtforms import StringField, TextField, PasswordField, BooleanField, FileField, TextAreaField 
from wtforms.validators import ( ValidationError, StopValidation, 
    InputRequired, Required, Length, Regexp, EqualTo, Email )
from models import User

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'error')

class LoginForm(Form):
    '''
    用户登陆
    '''
    name = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('password', validators=[InputRequired('Please enter your password.')])
    remember_me = BooleanField('remember_me', default=False)

class RegistrationForm(Form):
    '''
    用户注册
    '''
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

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class ImageUploadForm(Form):
    '''
    图片上传
    '''
    image = FileField(u'Image File')
    description  = TextAreaField(u'Image Description')

    def validate_image(self, field):
        if field.data is None or imghdr.what('unused', field.data.read()) is None:
            message = self.message or 'An image file is required'
            raise StopValidation(message)