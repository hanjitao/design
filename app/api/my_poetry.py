from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Poems, Loved_Poetry, New_Poetry, User_Action, Draft, Appraise

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
    if not poetrys:
        return jsonify({
            'title': '喜欢的诗',
            'subjects': []
        })
    return jsonify({
        'title': '喜欢的诗',
        'subjects': res
    })

@api.route('/get_new_poetry_by_id')
def get_new_poetry_by_id():
    id = request.args.get('id', 0)
    user_id = request.args.get('user_id', 0)
    id = int(id)
    user_id = int(user_id)
    poetry = New_Poetry.query.filter(New_Poetry.id == id).first()
    action = User_Action.query.filter(User_Action.user_id == user_id, User_Action.pid == id).first()
    res = poetry.to_dict()

    if action:
        print(action.praise)
        print(action.collect)
        print(action.id)
        print(action.user_id)
        print(action.pid)
        res['praise']=action.praise
        res['collect']=action.collect
    else:
        res['praise']=0
        res['collect']=0
    print("-------------------OVER")
    print(id)

    print(res)
    #loved_poetry = {}
    if not poetry:
        return jsonify({
            'title': '喜欢的诗',
            'subjects': {}
        })
    return jsonify({
        'title': '诗',
        'subjects': res
    })


@api.route('/get_my_poetry')
def get_my_poetry():
    user_id = request.args.get('user_id', 0)
    flag = request.args.get('flag', -1)
    user_id = int(user_id)
    flag = int(flag)
    print(user_id)

    poetrys = New_Poetry.query.filter(New_Poetry.creator_id==user_id,New_Poetry.public==0, New_Poetry.save==1).all()

    res = []
    if flag == -1:
        for poetry in poetrys[0:20]:
            res.append(poetry.to_dict())
    else:
        num = 0
        for poetry in poetrys:
            if poetry.id == flag:
                num = 1
            if num > 0 and num <= 20:
                res.append(poetry.to_dict())
                num += 1

    print('res is',res)
    if not poetrys:
        return jsonify({
            'title': '我的保存',
            'subjects': []
        })
    return jsonify({
        'title': '我的保存',
        'subjects': res
    })

@api.route('/get_my_public')
def get_my_public():
    user_id = request.args.get('user_id', 0)
    flag = request.args.get('flag', -1)
    user_id = int(user_id)
    flag = int(flag)

    poetrys = New_Poetry.query.filter(New_Poetry.creator_id==user_id , New_Poetry.public==1, \
                                      New_Poetry.save==1).all()

    res = []
    for poetry in poetrys:
        res.append(poetry.to_dict())
    if not poetrys:
        return jsonify({
            'title': '我的发布',
            'subjects': []
        })
    return jsonify({
        'title': '我的发布',
        'subjects': res
    })

@api.route('/get_my_praise')
def get_my_praise():
    user_id = request.args.get('user_id', 0)
    flag = request.args.get('flag', -1)
    user_id = int(user_id)
    flag = int(flag)

    user_action_all= User_Action.query.filter_by(user_id=user_id, praise=1).all()
    pids = [user_action.pid for user_action in user_action_all]
    poetrys = New_Poetry.query.filter(New_Poetry.id.in_(pids)).all()

    res = []
    if flag == -1:
        for poetry in poetrys[0:20]:
            res.append(poetry.to_dict())
    else:
        num = 0
        for poetry in poetrys:
            if poetry.id == flag:
                num = 1
            if num > 0 and num <= 20:
                res.append(poetry.to_dict())
                num += 1

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
    flag = request.args.get('flag', -1)
    user_id = int(user_id)
    flag = int(flag)

    user_action_all= User_Action.query.filter_by(user_id=user_id, collect=1).all()
    pids = [user_action.pid for user_action in user_action_all]
    poetrys = New_Poetry.query.filter(New_Poetry.id.in_(pids)).all()

    res = []
    if flag == -1:
        for poetry in poetrys[0:20]:
            res.append(poetry.to_dict())
    else:
        num = 0
        for poetry in poetrys:
            if poetry.id == flag:
                num = 1
            if num > 0 and num <= 20:
                res.append(poetry.to_dict())
                num += 1

    if not poetrys:
        return jsonify({
            'title': '我的作品',
            'subjects': []
        })
    return jsonify({
        'title': '我的收藏',
        'subjects': res
    })

@api.route('/get_waste_poetry')
def get_waste_poetry():
    user_id = request.args.get('user_id', 0)
    flag = request.args.get('flag', -1)
    user_id = int(user_id)
    flag = int(flag)

    poetrys = New_Poetry.query.filter(New_Poetry.creator_id==user_id, New_Poetry.save==0).all()
    res = []
    if flag == -1:
        for poetry in poetrys[0:20]:
            res.append(poetry.to_dict())
    else:
        num = 0
        for poetry in poetrys:
            if poetry.id == flag:
                num = 1
            if num > 0 and num <= 20:
                res.append(poetry.to_dict())
                num += 1

    if not poetrys:
        return jsonify({
            'title': '废纸篓',
            'subjects': []
        })
    return jsonify({
        'title': '废纸篓',
        'subjects': res
    })


@api.route('/send_appraise')
def send_appraise():
    user_id = request.args.get('userId', 0)
    poeticness = request.args.get('poeticness', 10)
    fluency = request.args.get('fluency', 10)
    coherence = request.args.get('coherence', 10)
    meaning = request.args.get('meaning', 10)
    message = request.args.get('message', '')

    try:
        appraise = Appraise(user_id, poeticness, fluency, coherence, meaning, message)
        db.session.add(appraise)
        db.session.commit()
        return jsonify({
            'title': '反馈成功',
            'success': 1,
        })
    except Exception as e:
        return jsonify({
            'title': '反馈失败',
            'error': 1,
        })

