#!/usr/bin/python
# -*- coding: utf-8 -*-

from werkzeug import secure_filename
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from ..forms import ImageUploadForm
from PIL import Image, ImageFile
from gevent.event import AsyncResult, Timeout
from gevent.queue import Empty, Queue
from hashlib import sha1
from stat import S_ISREG, ST_CTIME, ST_MODE

bt_image = Blueprint('image', __name__, template_folder='templates')

broadcast_queue = Queue()

def broadcast(message):
    '''
    Notify all waiting gthreads of message.
    '''
    waiting = []
    try:
        while True:
            waiting.append(broadcast_queue.get(block=False))
    except Empty:
        pass
    print('Broadcasting {0} messages'.format(len(waiting)))
    for item in waiting:
        item.set(message)

def receive():
    '''
    Generator that yields a message at least every KEEP_ALIVE_DELAY seconds.
    yields messages sent by broadcast
    '''
    now = time.time()
    end = now + MAX_DURATION
    tmp = None

    while now < end:
        if not tmp:
            tmp = AsyncResult()
            broadcast_queue.put(tmp)
        try:
            yield tmp.get(timeout=KEEP_ALIVE_DELAY)
            tmp = None
        except Timeout:
            yield ''
        now = time.time()

def save_normalized_image(path, data):
    image_parser = ImageFile.Parser()
    try:
        image_parser.feed(data)
        image = image_parser.close()
    except IOError:
        raise
        return False
    image.thumbnail(MAX_IMAGE_SIZE, Image.ANTIALIAS)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(path)
    return True

def event_stream(client):
    force_disconnect = False
    try:
        for message in receive():
            yield 'data: {0}\n\n'.format(message)
        print('{0} force closing stream'.format(client))
        force_disconnect = True
    finally:
        if not force_disconnect:
            print('{0} disconnected from stream'.format(client))

@bt_image.route('/post', methods=('POST'))
def post():
    form = ImageUploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        form.image.data.save('yile/static/uploads/abc.jpg')
        
    return render_template('admin/index.html', form=form)

