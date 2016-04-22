#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask.ext.login import LoginManager
from models import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)