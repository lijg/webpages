#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from ..models import Image, Category

bt_pages = Blueprint('pages', __name__, template_folder='templates')

@bt_pages.route('/')
def index():
	try:
		category = Category.query.filter_by(name=u'轮播图片').first()
		if category is not None:
			return render_template('index.html', head_images=category.image)
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
