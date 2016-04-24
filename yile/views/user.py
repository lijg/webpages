#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, redirect, request, url_for, flash
from jinja2 import TemplateNotFound
from flask.ext.login import current_user, login_user, logout_user, login_required
from ..login import login_manager
from ..forms import LoginForm, RegistrationForm
from ..models import db, User

bt_user = Blueprint('user', __name__, template_folder='templates')

@bt_user.route('/')
def index():
    try:
        return render_template('admin/user.html')
    except TemplateNotFound:
        abort(404)

@bt_user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('pages.index'))

    form = LoginForm()
    if form.validate_on_submit():        
        name = form.name.data.strip()
        password = form.password.data.strip()
        remember_me = form.remember_me.data

        user = User.query.filter_by(name=name).first()

        if user is not None and user.verify_password(password):
            login_user(user, remember_me)
            return redirect(request.args.get('next') or url_for('pages.index'))
        else:
            flash('Error Name or Password.')

    return render_template('admin/login.html', form=form)

@bt_user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('pages.index'))

@bt_user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('pages.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data.strip(),
                    email=form.email.data.strip(),
                    password=form.password.data.strip())
        db.session.add(user)
        db.session.commit()
        flash('register successfully, please login')
        return redirect(url_for('user.login'))
    return render_template('admin/register.html', form=form)