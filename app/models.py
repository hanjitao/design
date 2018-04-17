#!/usr/bin/env python
# coding=utf-8
from . import db, login_manager
from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from datetime import datetime
from .utils import splite_poetry
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from app.exceptions import ValidationError

class Poems(db.Model):
    __tablename__ = 'poems'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, primary_key=True)
    dynasty = db.Column(db.String(10), nullable=False)
    author = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return 'Poems %r' % self.title

    # 序列化转换: 资源->JSON
    def to_json(self):
        json_poem = {
            'title'  : self.title,
            'content'  : self.content,
            'author'  : self.author,
            'dynasty'  : self.dynasty,
        }
        return json_poem

class Loved_Poetry(db.Model):
    __tablename__ = 'loved_poetry'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return 'Poems %r' % self.title

    # 序列化转换: 资源->JSON
    def to_dict(self):
        loved_poetry_dict = {
            'type'  : self.type,
            'content'  : self.content,
            'title'  : self.title,
        }
        return loved_poetry_dict

class New_Poetry(db.Model):
    __tablename__ = 'new_poetry'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, nullable=False)
    creator_name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    input = db.Column(db.Text, nullable=False)
    extra = db.Column(db.Text, nullable=False)
    praise_num = db.Column(db.Integer, nullable=False)
    collect_num = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.Integer, nullable=False)
    public_time = db.Column(db.Integer, nullable=False)
    auto = db.Column(db.Integer, nullable=False)
    public = db.Column(db.Integer, nullable=False)
    save = db.Column(db.Integer, nullable=False)

    def __init__(self, creator_id, creator_name, type, title, content, input, create_time, auto):
        self.creator_id = creator_id,
        self.creator_name = creator_name,
        self.type = type,
        self.title = title,
        self.content = content,
        self.input = input,
        self.create_time = create_time,
        self.auto = auto
        self.praise_num = 0
        self.collect_num = 0

    def __repr__(self):
        return 'Poems %r' % self.title

    # 序列化转换: 资源->JSON
    def to_dict(self):
        print('to dict int', self.content)
        print(type(self.content))
        new_poetry_dict = {
            'id'  : self.id,
            'creator_id' : self.creator_id,
            'creator_name' : self.creator_name,
            'type' : self.type,
            'content' : self.content,
            'title' : self.title,
            'input' : self.input,
            'extra' : self.extra,
            'praise_num' : self.praise_num,
            'collect_num' : self.collect_num,
            'create_time' : self.create_time,
            'public_time' : self.public_time,
            'auto' : self.auto,
            'public' : self.public,
            'save' : self.save,
            'sentence' : splite_poetry(self.content)
        }
        return new_poetry_dict

class User_Action(db.Model):
    __tablename__ = 'user_action'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    praise = db.Column(db.Integer, nullable=False)
    collect = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'User_Action %r' % self.title

