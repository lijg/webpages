#!/usr/bin/python
# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    '''
    分类
    '''  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(1024))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        """
        Returns name
        """
        return '<Category %r>' % self.name

    def save(self):
        """
        保存到数据库中
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''
        删除数据
        '''
        db.session.delete(self)
        db.session.commit()

class Tag(db.Model):
    '''
    标签
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(1024))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        """
        Returns name
        """
        return '<ImageCategory %r>' % self.name

    def save(self):
        """
        保存到数据库中
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''
        删除数据
        '''
        db.session.delete(self)
        db.session.commit()

class Image(db.Model):
    '''
    图片
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(1024))
    description = db.Column(db.String(1024))

    # 用于外键的字段
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # 外键对象，不会生成数据库实际字段
    # backref指反向引用，也就是外键Category通过backref(image)查询Image
    category = db.relationship('Category', backref=db.backref('image', lazy='dynamic'))

    def __unicode__(self):
        return self.path

    def __init__(self, path, description, category_id):
        self.path = path
        self.description = description
        self.category_id = category_id

    def save(self):
        """
        保存到数据库中
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(db.Model):
    '''
    用户
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
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
        """
        校验密码是否正确
        """
        return check_password_hash(self.password, password)  

    def save(self):
        """
        保存到数据库中
        """
        db.session.add(self)
        db.session.commit()

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

