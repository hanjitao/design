from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Poems, Attention, Loved_Poetry, New_Poetry, User_Action, User
import socket
import time
import json
import random

def get_poetry(describe, ptype):

    print('type uis ...........')
    print(ptype)
    #port = 8080 if ptype == 5 else 8081
    a=random.randint(0,1)
    if a:
        port = 8081
    else:
        port = 8082
    print("port is", port)
    client = socket.socket()
    client.connect(('localhost',port))

    if not describe:
        describe = '春'

    client.send(describe.encode('utf-8'))
    data = client.recv(1024).decode()
    a = data.split('|')
    title = a[0]
    content = a[1]
    print('title is', title)
    print('content is', content)
    client.close()
    return title, content



@api.route('/generate_new_poetry')
def generate_new_poetry():
    user_id = request.args.get('user_id', 0)
    user_name = request.args.get('user_name', 'visitor')
    if user_id == 'undefined':
        user_id = 0
        print('user_id is undefined')
    user_id = int(user_id)
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        user_name = user.nickName
    ptype = request.args.get('type',5)
    ptype = int(ptype)
    auto = request.args.get('auto',1)
    describe = request.args.get('describe','')
    title = request.args.get('title','')
    if not title:
        title = '无题'

    print("eeeeeeeeeeeeeeeeeeeee", user_name, user_id)
    create_time = int(time.time())

    if auto:
        title,  content = get_poetry(describe, ptype)
    else:
        content = request.args.get('content', '')

    poetry = New_Poetry(user_id, user_name, ptype, title, content, describe, create_time, 0)
    db.session.add(poetry)
    db.session.commit()

    res = poetry.to_dict()

    db.session.delete(poetry)
    db.session.commit()

    if not res:
        return jsonify({
            'title': '生成失败',
            'subjects': {}
        })
    return jsonify({
        'title': '自动写诗',
        'subjects': res,
    })

@api.route('/user_action')
def user_action():
    user_id = request.args.get('user_id', 0)
    pid = request.args.get('id', 0)
    if not pid:
        return jsonify({
            'message': 'no id'
        })
    praise = request.args.get('praise',0)
    collect = request.args.get('collect',0)
    save = request.args.get('save',1)

    try:
        print("test start.....................")
        poetry = New_Poetry.query.filter_by(id=pid).first()

        print("test start.....................")
        try:
            action = User_Action.query.filter(User_Action.user_id == user_id, User_Action.pid == pid).first()
        except Exception as e:
            print('error is',e)
        print(action)
        print("test start.....................")
        if not action:
            action = User_Action(user_id ,pid,praise,collect)
            db.session.add(action)
            print("not have it")
        else:
            action.praise += int(praise)
            action.collect += int(collect)
            print("have it")

        poetry = New_Poetry.query.filter_by(id=pid).first()
        poetry.collect_num += int(collect)
        poetry.praise_num += int(praise)
        poetry.save = save
        db.session.commit()

        res = poetry.to_dict()
        res['praise'] = action.praise
        res['collect'] = action.collect
        print('user_action res is', res)
        return jsonify({
            'message': 'success',
            'subjects': res,
        })
    except Exception as e:
        return jsonify({
            'message' : 'db error'
        })

@api.route('/save_poetry')
def save_poetry():
    poetry = request.args.get('poetry')
    poetry = json.loads(poetry)

    pid = poetry.get('id',0)
    user_id = poetry.get('creator_id',0)
    user_name = poetry.get('creator_name','-')
    if not user_id:
        user_id = poetry.get('user_id',0)
        user = User.query.filter(User.id == user_id).first()
        user_name = user.nickName
        print("eeeeeeeeeeeeeeeeeeeee", user_name, user_id)

    content = poetry.get('content','-')
    describe = poetry.get('input','')
    create_time = poetry.get('create_time', int(time.time()))
    title = poetry.get('title','无题')
    ptype = poetry.get('type',5)

    if title == '':
        title = '无题'
    print("title is", title)
    poetry = New_Poetry.query.filter(New_Poetry.id==pid).first()
    print(poetry)
    print("========================")
    if not poetry:
        poetry = New_Poetry(user_id, user_name, ptype, title, content, describe, create_time, 1)
        db.session.add(poetry)
        print('not have it')
    else:
        print('have it')
        poetry.content = content
        poetry.title = title

    db.session.commit()

    if not poetry:
        return jsonify({
            'title': '喜欢的诗',
            'subjects': {}
        })
    return jsonify({
        'title': '自动写诗',
        'subjects': poetry.to_dict(),

    })

@api.route('/modify_attention')
def modify_attention():
    user_id = request.args.get('user_id', 0)
    attention_uid = request.args.get('attention_uid', 0)
    status = request.args.get('status',0)
    user_id = int(user_id)
    attention_uid = int(attention_uid)
    status = int(status)
    try:
        attention = Attention.query.filter(Attention.user_id == user_id, \
                    Attention.attention_uid == attention_uid).first()
        if not attention:
            attention = Attention(user_id, attention_uid, status)
            db.session.add(attention)
        else:
            attention.status = status

        db.session.commit()

        res = {}
        return jsonify({
            'message': 'success',
            'subjects': res,
        })
    except Exception as e:
        return jsonify({
            'message' : 'error'
        })

@api.route('/get_attention_list')
def get_attention_list():
    user_id = request.args.get('user_id', 0)
    user_id = int(user_id)
    try:
        attentions = Attention.query.filter(Attention.user_id == user_id, \
                    Attention.status == 1).all()

        uids = [ a.attention_uid for a in attentions]
        users = User.query.filter(User.id.in_(uids)).all()
        res = []
        for user in users:
            res.append(user.to_dict())

        return jsonify({
            'message': 'success',
            'subjects': res,
        })
    except Exception as e:
        return jsonify({
            'message' : 'error'
        })

@api.route('/get_hotkeys')
def get_hotkeys():
    user_id = request.args.get('user_id', 0)
    user_id = int(user_id)

    res = ['春天','忧伤','开心','孤独','一阵微风吹过']
    return jsonify({
        'subjects': res,
    })


