from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Poems, Loved_Poetry, New_Poetry, User_Action

@api.route('/get_newest_rank')
def get_newest_rank():

    poetrys = New_Poetry.query.order_by(New_Poetry.public_time.desc()).all()

    res = []
    for poetry in poetrys:
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

    poetrys = New_Poetry.query.order_by(New_Poetry.public_time.desc()).all()

    res = []
    for poetry in poetrys:
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

    poetrys = New_Poetry.query.order_by(New_Poetry.praise_num.desc()).all()

    res = []
    for poetry in poetrys:
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

    poetrys = New_Poetry.query.order_by(New_Poetry.collect_num.desc()).all()

    res = []
    for poetry in poetrys:
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

