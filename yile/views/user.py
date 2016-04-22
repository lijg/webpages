#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, redirect, request, url_for, g
from jinja2 import TemplateNotFound
from ..login import login_manager
from ..forms import LoginForm

bt_user = Blueprint('user', __name__, template_folder='templates')

@bt_user.route('/')
def index():
	try:
		return render_template('admin/user.html')
	except TemplateNotFound:
		abort(404)

@bt_user.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('pages.index'))

    form = LoginForm()
    if form.validate_on_submit():        
        name = form.name.data.strip()
        password = form.password.data.strip()
        remember_me = form.remember_me.data


        # login_manager.login_user(user)

        # flash('Logged in successfully.')

        # next = request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        # if not next_is_valid(next):
            # return abort(400)
        # return redirect(next or flask.url_for('pages.index'))
        return redirect(url_for('pages.index'))

    return render_template('admin/login.html', form=form)

@bt_user.route('/logout')
def logout():
	try:
		return render_template('admin/logout.html')
	except TemplateNotFound:
		abort(404)

@bt_user.route('/forget')
def forget():
	try:
		return render_template('admin/logout.html')
	except TemplateNotFound:
		abort(404)
