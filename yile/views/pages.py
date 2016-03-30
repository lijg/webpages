#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

bt_pages = Blueprint('pages', __name__, template_folder='templates')

@bt_pages.route('/')
def index():
	try:
		return render_template('index.html')
	except TemplateNotFound:
		abort(404)

@bt_pages.route('/gallery')
def gallery():
	try:
		return render_template('gallery.html')
	except TemplateNotFound:
		abort(404)

@bt_pages.route('/contact')
def contact():
	try:
		return render_template('contact.html')
	except TemplateNotFound:
		abort(404)
