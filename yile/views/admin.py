#!/usr/bin/python
# -*- coding: utf-8 -*-

from werkzeug import secure_filename
from flask import Blueprint, render_template, abort, flash, redirect, url_for
from jinja2 import TemplateNotFound
from ..forms import flash_errors, ImageUploadForm, CategoryForm, TagForm
from ..models import Category, Tag

bt_admin = Blueprint('admin', __name__, template_folder='templates')

@bt_admin.route('/', methods=('GET', 'POST'))
def index():
    form = ImageUploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        form.image.data.save('yile/static/uploads/abc.jpg')
        
    return render_template('admin/index.html', form=form)

@bt_admin.route('/category', methods=('GET', 'POST'))
def category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name = form.name.data.strip(),
                            description = form.description.data.strip())
        category.save()
        flash('add successfully')
        return redirect(url_for('admin.category'))
    else:
        flash_errors(form)
    return render_template('admin/category.html', form=form,
        categories=Category.query.all())

@bt_admin.route('/category/del/<int:category_id>')
def del_category(category_id):
    category = Category.query.filter_by(id=category_id).first()
    name = category.name
    category.delete()
    flash('category <%s> has been removed' % name)
    return redirect(url_for('admin.category'))

@bt_admin.route('/tag', methods=('GET', 'POST'))
def tag():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name = form.name.data.strip(),
                            description = form.description.data.strip())
        tag.save()
        flash('add successfully')
        return redirect(url_for('admin.tag'))
    else:
        flash_errors(form)
    return render_template('admin/tag.html', form=form,
        tags=Tag.query.all())

@bt_admin.route('/tag/del/<int:tag_id>')
def del_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    name = tag.name
    tag.delete()
    flash('tag <%s> has been removed' % name)
    return redirect(url_for('admin.tag'))

@bt_admin.route('/photo', methods=('GET', 'POST'))
def photo():
    return render_template('admin/photo.html')

@bt_admin.route('/user', methods=('GET', 'POST'))
def user():
    return render_template('admin/user.html', users=User.query.all())