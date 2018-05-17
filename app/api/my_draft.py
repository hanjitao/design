from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Poems, Loved_Poetry, New_Poetry, User_Action, Draft
import json

@api.route('/get_my_draft')
def get_my_draft():
    user_id = request.args.get('user_id', 0)
    user_id = int(user_id)

    drafts = Draft.query.filter(Draft.user_id == user_id, Draft.finish == 0, Draft.dele == 0).all()
    res = []

    for draft in drafts:
        res.append(draft.to_dict())

    if not res:
        return jsonify({
            'title': '我的草稿',
            'subjects': []
        })
    return jsonify({
        'title': '我的草稿',
        'subjects': res
    })


@api.route('/edit_draft')
def edit_draft():
    id = request.args.get('id', 0)
    id = int(id)

    draft = Draft.query.filter(Draft.id == id).first()

    if not draft:
        return jsonify({
            'title': '编辑',
            'subjects': {}
        })
    return jsonify({
        'title': '编辑',
        'subjects': draft.to_dict()
    })

@api.route('/new_draft')
def new_draft():
    user_id = request.args.get('user_id', 0)
    user_id = int(user_id)

    draft = Draft(user_id, '')
    db.session.add(draft)
    db.session.commit()

    if not draft:
        return jsonify({
            'title': '新建',
            'subjects': {}
        })
    return jsonify({
        'title': '新建',
        'subjects': draft.to_dict()
    })

@api.route('/delete_draft')
def delete_draft():
    id = request.args.get('id', 0)
    id = int(id)

    draft = Draft.query.filter(Draft.id == id).first()
    draft.dele = 1
    db.session.commit()

    if not draft:
        return jsonify({
            'title': '删除失败',
            'subjects': {}
        })
    return jsonify({
        'title': '删除成功',
        'subjects': draft.to_dict()
    })

@api.route('/finish_draft')
def finish_draft():
    id = request.args.get('id', 0)
    id = int(id)

    draft = Draft.query.filter(Draft.id == id).first()
    draft.finish = 1
    db.session.commit()

    if not draft:
        return jsonify({
            'title': '删除失败',
            'subjects': {}
        })
    return jsonify({
        'title': '删除成功',
        'subjects': draft.to_dict()
    })

@api.route('/save_draft')
def save_draft():
    poetry = request.args.get('poetry')
    poetry = json.loads(poetry)
    id = poetry.get('id',0)
    draft = Draft.query.filter(Draft.id == id).first()
    draft.sentence1 = poetry.get('sentence1', draft.sentence1)
    draft.sentence2 = poetry.get('sentence2', draft.sentence2)
    draft.sentence3 = poetry.get('sentence3', draft.sentence3)
    draft.sentence4 = poetry.get('sentence4', draft.sentence4)
    draft.title = poetry.get('title', draft.title)

    db.session.commit()

    if not draft:
        return jsonify({
            'title': '保存失败',
            'subjects': {}
        })
    return jsonify({
        'title': '保存成功',
        'subjects': draft.to_dict()
    })

