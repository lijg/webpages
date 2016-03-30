#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_admin import Admin
from views.pages import bt_pages
from views.admins import admin_ImageView
from models import db, Image

admin = Admin(name="YILE", template_mode='bootstrap3')

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    db.init_app(app)
    admin.init_app(app)

    with app.app_context():
        db.create_all()

	admin_ImageView.upload_image_path = app.config['UPLOAD_IMAGE_PATH']
    admin.add_view(admin_ImageView(Image, db.session))

    app.register_blueprint(bt_pages)

    return app
