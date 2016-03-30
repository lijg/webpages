#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
            os.path.pardir))

DEBUG = True

CSRF_ENABLED = True

SQLALCHEMY_ECHO = True

SECRET_KEY = 'dF65C43128B4d9cB'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "data", "data.db")

UPLOAD_IMAGE_PATH = os.path.join(basedir, "yile", "static", "images")