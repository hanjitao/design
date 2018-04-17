from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Poems, Loved_Poetry, New_Poetry, User_Action

@api.route('/query_poems_by_title')
def query_poems_by_title():
    title = request.args.get('title','')
    poems = Poems.query.filter_by(title=title).first()
    if not poems:
        return jsonify({})

    return jsonify(poems.to_json())

@api.route('/query_poems_by_author')
def query_poems_by_author():
    author = request.args.get('author','')
    poems = Poems.query.filter_by(author=author).first()
    if not poems:
        return jsonify({})

    return jsonify(poems.to_json())

@api.route('/get_loved_poetry')
def get_loved_poetry():
    user_id = request.args.get('user_id', 0)
    print(user_id)
    poetrys = Loved_Poetry.query.filter_by(user_id=user_id).all()

    #loved_poetry = {}
    res = []
    for poetry in poetrys:
        res.append(poetry.to_dict())
    print(poetrys)
    if not poetrys:
        return jsonify({
            'title': '喜欢的诗',
            'subjects': []
        })
    return jsonify({
        'title': 'test',
        'subjects': res
    })

@api.route('/get_new_poetry_by_id')
def get_new_poetry_by_id():
    id = request.args.get('id', 0)
    print(id)
    poetry = New_Poetry.query.filter_by(id=id).first()

    #loved_poetry = {}
    if not poetry:
        return jsonify({
            'title': '喜欢的诗',
            'subjects': {}
        })
    return jsonify({
        'title': 'test',
        'subjects': poetry.to_dict()
    })

@api.route('/get_my_poetry')
def get_my_poetry():
    user_id = request.args.get('user_id', 1)
    print(user_id)
    poetrys = New_Poetry.query.filter_by(creator_id=user_id).all()

    res = []
    for poetry in poetrys:
        res.append(poetry.to_dict())
    if not poetrys:
        return jsonify({
            'title': '我的作品',
            'subjects': []
        })
    return jsonify({
        'title': 'test',
        'subjects': res
    })

@api.route('/get_my_public')
def get_my_public():
    user_id = request.args.get('user_id', 1)
    print(user_id)
    poetrys = New_Poetry.query.filter(New_Poetry.creator_id==user_id , New_Poetry.public==1).all()

    res = []
    for poetry in poetrys:
        res.append(poetry.to_dict())
    if not poetrys:
        return jsonify({
            'title': '我的作品',
            'subjects': []
        })
    return jsonify({
        'title': 'test',
        'subjects': res
    })

@api.route('/get_my_praise')
def get_my_praise():
    user_id = request.args.get('user_id', 1)
    user_action_all= User_Action.query.filter_by(user_id=user_id, praise=1).all()
    pids = [user_action.pid for user_action in user_action_all]
    poetrys = New_Poetry.query.filter(New_Poetry.id.in_(pids)).all()

    res = []
    for poetry in poetrys:
        res.append(poetry.to_dict())
    if not poetrys:
        return jsonify({
            'title': '我的点赞',
            'subjects': []
        })
    return jsonify({
        'title': '我的点赞',
        'subjects': res
    })

@api.route('/get_my_collect')
def get_my_collect():
    user_id = request.args.get('user_id', 1)
    user_action_all= User_Action.query.filter_by(user_id=user_id, collect=1).all()
    pids = [user_action.pid for user_action in user_action_all]
    poetrys = New_Poetry.query.filter(New_Poetry.id.in_(pids)).all()

    res = []
    for poetry in poetrys:
        res.append(poetry.to_dict())
    if not poetrys:
        return jsonify({
            'title': '我的作品',
            'subjects': []
        })
    return jsonify({
        'title': 'test',
        'subjects': res
    })

@api.route('/get_waste_poetry')
def get_waste_poetry():
    user_id = request.args.get('user_id', 1)
    print(user_id)
    poetrys = New_Poetry.query.filter(New_Poetry.creator_id==user_id, New_Poetry.save==0).all()

    res = []
    for poetry in poetrys:
        res.append(poetry.to_dict())
    if not poetrys:
        return jsonify({
            'title': '废纸篓',
            'subjects': []
        })
    return jsonify({
        'title': 'test',
        'subjects': res
    })

