#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from views import bt_pages, bt_admin, bt_user
from models import db
from login import login_manager

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(bt_pages)
    app.register_blueprint(bt_admin, url_prefix='/admin')
    app.register_blueprint(bt_user, url_prefix='/user')

    return app
