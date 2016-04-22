#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

bt_admin = Blueprint('admin', __name__, template_folder='templates')

@bt_admin.route('/')
def index():
	try:
		return render_template('admin/index.html')
	except TemplateNotFound:
		abort(404)

