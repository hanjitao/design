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

class User_Action(db.Model):
    __tablename__ = 'user_action'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    praise = db.Column(db.Integer, nullable=False)
    collect = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'User_Action'

    def __init__(self, user_id, pid, praise, collect):
        self.user_id = user_id,
        self.pid = pid,
        self.praise = praise,
        self.collect = collect,


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
    praise_num = db.Column(db.Integer, default=0)
    collect_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.Integer, nullable=False)
    public_time = db.Column(db.Integer, nullable=False)
    auto = db.Column(db.Integer, nullable=False)
    public = db.Column(db.Integer, default=0)
    save = db.Column(db.Integer, default=0)
    image_name = db.Column(db.String(150), nullable=False)

    def __init__(self, creator_id, creator_name, type, title, content, input, create_time, save):
        self.creator_id = creator_id,
        self.creator_name = creator_name,
        self.type = type,
        self.title = title,
        self.content = content,
        self.input = input,
        self.create_time = create_time,
        self.save = save

    def __repr__(self):
        return 'Poems %r' % self.title

    # 序列化转换: 资源->JSON
    def to_dict(self):
        try:
            sentence = splite_poetry(self.content)
        except Exception as e:
            sentence = splite_poetry('春草风香怨，西东水上荆。流莺尝绣袂，未可见花英。')
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
            'sentence1' : sentence['first'],
            'sentence2' : sentence['second'],
            'sentence3' : sentence['third'],
            'sentence4' : sentence['forth'],
            'image_name' : self.image_name
        }
        return new_poetry_dict


####### class User --> table users
class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  openId = db.Column(db.String(50), unique=True, nullable=False)
  nickName = db.Column(db.String(100), nullable=False)
  gender = db.Column(db.Integer)
  city = db.Column(db.String(40))
  province = db.Column(db.String(40))
  country = db.Column(db.String(40))
  avatarUrl = db.Column(db.String(200))
  createTime = db.Column(db.DateTime, index=True, default=datetime.now())

  def __repr__(self):
    return 'User %r' % self.nickName

  # 序列化转换: 资源->JSON
  def to_dict(self):
    dict_user = {
      'id' : self.id,
      'nickName'  : self.nickName,
      'gender'  : self.gender,
      'city'  : self.city,
      'province'  : self.province,
      'country'  : self.country,
      'avatarUrl'  : self.avatarUrl,
    }
    return dict_user


  # 生成授权token
  def generate_auth_token(self, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'openId': self.openId})

  # 验证授权token
  @staticmethod
  def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      data = s.loads(token)
      print(data)
    except:
      return None
    return User.query.filter_by(openId=data['openId']).first()


# user_loader回调，用于从会话中存储的用户ID重新加载用户对象
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


####### class AnonymousUser --> no table
class AnonymousUser(AnonymousUserMixin):
  def can(self, permissions):
    return False

  def is_administrator(self):
    return False
login_manager.anonymous_user = AnonymousUser

class Draft(db.Model):
    __tablename__ = 'draft'
    id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(100), default="")
    content = db.Column(db.String(200), default="")
    describe = db.Column(db.String(200), default="")
    finish = db.Column(db.Integer, default=0)
    modify_time = db.Column(db.DateTime, default=datetime.now())
    dele = db.Column(db.Integer, default=0)
    sentence1= db.Column(db.String(50), default="")
    sentence2= db.Column(db.String(50), default="")
    sentence3= db.Column(db.String(50), default="")
    sentence4= db.Column(db.String(50), default="")

    def __repr__(self):
        return 'Draft %r' % self.title

    def __init__(self, user_id, title):
        self.user_id = user_id,
        self.title = title,

    # 序列化转换: 资源->JSON
    def to_dict(self):
        print('----------------',type(self.modify_time))
        print('modify_time is', self.modify_time)
        time_str = self.modify_time.strftime('%Y年%m月%d日 %H:%M')
        dict_draft = {
            'id' : self.id,
            'user_id' : self.user_id,
            'title'  : self.title,
            'content'  : self.content,
            'describe' : self.describe,
            'modify_time' : time_str,
            'sentence1' : self.sentence1,
            'sentence2' : self.sentence2,
            'sentence3' : self.sentence3,
            'sentence4' : self.sentence4,
        }
        return dict_draft

class Appraise(db.Model):
    __tablename__ = 'appraise'
    id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    poeticness = db.Column(db.Integer, default=10)
    fluency = db.Column(db.Integer, default=10)
    coherence = db.Column(db.Integer, default=10)
    meaning = db.Column(db.Integer, default=10)
    message = db.Column(db.String(500), default="")
    create_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return 'Appraise..'

    def __init__(self, user_id, poeticness, fluency, coherence, meaning, message):
        self.user_id = user_id,
        self.poeticness =  poeticness,
        self.fluency = fluency,
        self.coherence = coherence,
        self.meaning = meaning,
        self.message = message,
