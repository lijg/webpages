#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import request, redirect, url_for
from flask_admin import form
from flask_admin.contrib import sqla
from jinja2 import Markup

    
class admin_ImageView(sqla.ModelView):

    upload_image_path = '/tmp'

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        print model.path

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.path)))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=upload_image_path,
                                      thumbnail_size=(100, 100, True))
    }


