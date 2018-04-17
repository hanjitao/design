from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Poems, Loved_Poetry, New_Poetry
import socket
import time


def get_poetry(describe, ptype):

    print('type uis ...........')
    print(ptype)
    port = 8080 if ptype == 5 else 8081
    client = socket.socket()
    client.connect(('localhost',port))

    if not describe:
        describe = '春'

    client.send(describe.encode('utf-8'))
    content = client.recv(1024).decode()

    client.close()
    return content



@api.route('/generate_new_poetry')
def generate_new_poetry():
    user_id = request.args.get('user_id', 1)
    user_name = request.args.get('user_name', '看不透')
    ptype = request.args.get('type',5)
    ptype = int(ptype)
    auto = request.args.get('auto',1)
    input = request.args.get('describe','')
    title = request.args.get('title','无题')
    describe = request.args.get('describe', '春')
    create_time = int(time.time())

    content = get_poetry(describe, ptype)

    poetry = New_Poetry(user_id, user_name, ptype, title, content, input, create_time, auto)
    db.session.add(poetry)
    db.session.commit()

    #poetry = New_Poetry.query.filter_by(id=id).first()

    #loved_poetry = {}
    if not poetry:
        return jsonify({
            'title': '喜欢的诗',
            'subjects': {}
        })
    return jsonify({
        'title': '自动写诗',
        'subjects': poetry.to_dict(),

    })

@api.route('/set_poetry_status')
def set_poetry_status():
    id = request.args.get('id', 0)
    if not id:
        return jsonify({
            'message': 'no id'
        })
    auto = request.args.get('auto',1)
    save = request.args.get('save',0)
    public = request.args.get('public',0)

    public_time = int(time.time()) if public else 0

    try:
        poetry = New_Poetry.query.filter_by(id=id).first()
        poetry.auto = auto
        poetry.save = save
        poetry.public = public
        poetry.public_time = public_time
        db.session.commit()
        return jsonify({
            'message': 'success',
            'subjects': poetry.to_dict(),
        })
    except Exception as e:
        return jsonify({
            'message' : 'db error'
        })


