#!/usr/bin/python
# -*- coding: utf-8 -*-

from werkzeug import secure_filename
from flask import Blueprint, render_template, abort, flash, redirect, url_for
from jinja2 import TemplateNotFound
from ..forms import flash_errors, ImageUploadForm, CategoryForm, TagForm, RoleForm
from ..models import Category, Tag, User, Image, Role
from flask.ext.login import login_required, current_user
from PIL import Image as PILImage

bt_admin = Blueprint('admin', __name__, template_folder='templates')

@bt_admin.before_request
def before_request():
    # 检查用户权限
    if current_user is not None and current_user.is_authenticated:
        pass
    else:
        return redirect(url_for('user.login'))

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
    form = ImageUploadForm()
    form.category_id.choices = [(g.id, g.name) for g in Category.query.order_by('name')]
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        filepath = 'yile/static/uploads/' + filename
        form.image.data.save(filepath)
        gen_thumbnail(filename)
        image = Image(filename, form.description.data.strip(), form.category_id.data)
        image.save()
        return redirect(url_for('admin.photo'))
    return render_template('admin/photo.html', form=form,
                    photos=Image.query.all())

def gen_thumbnail(filename):
    height = width = 128
    filepath = 'yile/static/uploads/' + filename
    thumbnailpath = 'yile/static/uploads/thumbnail/' + filename
    original = PILImage.open(filepath)
    thumbnail = original.resize((width, height), PILImage.ANTIALIAS)
    thumbnail.save(thumbnailpath)

@bt_admin.route('/photo/del/<int:photo_id>')
def del_photo(photo_id):
    image = Image.query.filter_by(id=photo_id).first()
    name = image.path
    image.delete()
    flash('Image <%s> has been removed' % name)
    return redirect(url_for('admin.photo'))


@bt_admin.route('/user', methods=('GET', 'POST'))
def user():
    return render_template('admin/user.html', users=User.query.all())

@bt_admin.route('/role', methods=('GET', 'POST'))
def role():
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name = form.name.data.strip(),
                            description = form.description.data.strip())
        role.save()
        flash('add successfully')
        return redirect(url_for('admin.role'))
    else:
        flash_errors(form)
    return render_template('admin/role.html', form=form,
        roles=Role.query.all())

@bt_admin.route('/role/del/<int:role_id>')
def del_role(role_id):
    role = Role.query.filter_by(id=role_id).first()
    name = role.name
    role.delete()
    flash('role <%s> has been removed' % name)
    return redirect(url_for('admin.role'))