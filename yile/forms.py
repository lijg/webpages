#!/usr/bin/python
# -*- coding: utf-8 -*-
import imghdr
from flask import flash
from flask_wtf import Form
from wtforms import StringField, TextField, PasswordField, BooleanField, FileField, TextAreaField, SelectField 
from wtforms.validators import ( ValidationError, StopValidation, 
    InputRequired, Required, Length, Regexp, EqualTo, Email )
from models import User, Category, Tag

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'error')

class CategoryForm(Form):
    '''
    增加分类
    '''
    name = StringField('Name', validators=[Required(), Length(1,64)])
    description = TextAreaField(u'Category Description')

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data.strip()).first():
            raise ValidationError('Name already in use.')

class TagForm(Form):
    '''
    增加分类
    '''
    name = StringField('Name', validators=[Required(), Length(1,64)])
    description = TextAreaField(u'Tag Description')

    def validate_name(self, field):
        if Tag.query.filter_by(name=field.data.strip()).first():
            raise ValidationError('Name already in use.')

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
        if User.query.filter_by(name=field.data.strip()).first():
            raise ValidationError('Name already in use.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.strip()).first():
            raise ValidationError('Email already registered.')

class ImageUploadForm(Form):
    '''
    图片上传
    '''
    image = FileField(u'Image File')
    description  = TextAreaField(u'Image Description')
    category_id = SelectField(u'Category', coerce=int)

    def validate_image(self, field):
        if field.data is None:
            message = self.message or 'An image file is required'
            raise StopValidation(message)

    def validate_category_id(self, field):
        if not Category.query.filter_by(id=field.data).first():
            raise ValidationError('Category does not exists.')