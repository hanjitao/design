from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Poems, Loved_Poetry, New_Poetry, User_Action

@api.route('/get_recommend_rank')
def get_recommend_rank():

    user_id = request.args.get('user_id', 0)
    flag = request.args.get('flag', -1)
    user_id = int(user_id)
    flag = int(flag)
    poetrys = New_Poetry.query.filter(New_Poetry.save==1, New_Poetry.public==1)\
        .order_by(New_Poetry.public_time.desc()).all()

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
                num += 1
                res.append(poetry.to_dict())

    if not poetrys:
        return jsonify({
            'title': '推荐',
            'subjects': []
        })
    return jsonify({
        'title': '推荐',
        'subjects': res
    })


@api.route('/get_newest_rank')
def get_newest_rank():

    user_id = request.args.get('user_id', 0)
    flag = request.args.get('flag', -1)
    user_id = int(user_id)
    flag = int(flag)

    poetrys = New_Poetry.query.filter(New_Poetry.save==1, New_Poetry.public==1)\
        .order_by(New_Poetry.public_time.desc()).all()

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
                num += 1
                res.append(poetry.to_dict())

    if not poetrys:
        return jsonify({
            'title': '最新榜',
            'subjects': []
        })
    return jsonify({
        'title': '最新榜',
        'subjects': res
    })

@api.route('/get_hottest_rank')
def get_hottest_rank():
    user_id = request.args.get('user_id', 0)
    flag = request.args.get('flag', -1)
    user_id = int(user_id)
    flag = int(flag)

    poetrys = New_Poetry.query.filter(New_Poetry.save==1, New_Poetry.public==1)\
        .order_by(New_Poetry.public_time.desc()).all()
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
                num += 1
                res.append(poetry.to_dict())

    if not poetrys:
        return jsonify({
            'title': '最热榜',
            'subjects': []
        })
    return jsonify({
        'title': '最热榜',
        'subjects': res
    })

@api.route('/get_praise_rank')
def get_praise_rank():
    user_id = request.args.get('user_id', 0)
    flag = request.args.get('flag', -1)
    user_id = int(user_id)
    flag = int(flag)

    poetrys = New_Poetry.query.filter(New_Poetry.save==1, New_Poetry.public==1)\
        .order_by(New_Poetry.praise_num.desc()).all()
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
                num += 1
                res.append(poetry.to_dict())

    if not poetrys:
        return jsonify({
            'title': '点赞榜',
            'subjects': []
        })
    return jsonify({
        'title': '点赞榜',
        'subjects': res
    })

@api.route('/get_collect_rank')
def get_collect__rank():
    user_id = request.args.get('user_id', 0)
    flag = request.args.get('flag', -1)
    user_id = int(user_id)
    flag = int(flag)

    poetrys = New_Poetry.query.filter(New_Poetry.save==1, New_Poetry.public==1)\
        .order_by(New_Poetry.collect_num.desc()).all()

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
                num += 1
                res.append(poetry.to_dict())
    if not poetrys:
        return jsonify({
            'title': '收藏榜',
            'subjects': []
        })
    return jsonify({
        'title': '收藏榜',
        'subjects': res
    })

@api.route('/get_city_rank')
def get_city_rank():

    poetrys = New_Poetry.query.order_by(New_Poetry.public_time.desc()).all()

    res = []
    for poetry in poetrys:
        res.append(poetry.to_dict())
    if not poetrys:
        return jsonify({
            'title': '同城圈',
            'subjects': []
        })
    return jsonify({
        'title': '同城圈',
        'subjects': res
    })


@api.route('/get_init_ranks')
def get_init_ranks():

    poetrys = New_Poetry.query.order_by(New_Poetry.collect_num.desc()).all()

    p = []
    for poetry in poetrys:
        p.append(poetry.to_dict())

    res = []
    for i in range(0,9):
        res.append(p)
    print('len is', len(res))
    if not poetrys:
        return jsonify({
            'title': '收藏榜',
            'subjects': []
        })
    return jsonify({
        'title': '收藏榜',
        'subjects': res
    })

