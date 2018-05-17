#!/usr/bin/env python
# coding=utf-8
from . import auth
from flask import request, current_app, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from app.exceptions import ValidationError
from ..models import User
from .. import db
import requests, json
from decimal import Decimal


@auth.route('/login', methods=['GET', 'POST'])
def login():
  code = request.args.get('code')
  encryptedData = request.args.get('encryptedData')
  rawData = request.args.get('rawData')
  signature = request.args.get('signature')
  iv = request.args.get('iv')

  # 用js_code，appid，secret，grant_type向微信服务器获取session_key,openid,expires_in
  data={}
  data['appid'] = current_app.config['APP_ID']
  data['secret'] = current_app.config['SECRET_KEY']
  data['js_code'] = code
  data['grant_type'] = 'authorization_code'
  res = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=data).json()
  print('weixin api: %s' % res)
  if 'session_key' in res:
    session_key = res['session_key']
    #expires_in = res['expires_in']
    openid = res['openid']
    print(rawData)
    print("-----------------------------------------")

    user = User.query.filter_by(openId=openid).first()
    is_first = True
    if user:
        print('user info is ', user.to_dict())
        login_user(user, True)
        return jsonify(user.to_dict())

    # 校验签名，判别数据完整性
    if sha1Sign(session_key, rawData) != signature:
      print(sha1Sign(session_key,rawData))
      print(signature)
      raise ValidationError('Invalid rawData!')
      return jsonify({'is_first':True})

    # 解密加密数据，校验appid
    if decrypt(session_key, encryptedData, iv) != data['appid']:
      print('invalid encryptedData')
      print(encryptedData)
      raise ValidationError('Invalid encryptedData!')
      return jsonify({'is_first':True})


    # 根据openid是否插入用户
    user = User.query.filter_by(openId=openid).first()
    print(rawData)
    print("-----------------------------------------")
    if user is None:
      print('add user: %s' % rawData)
      rData = json.loads(rawData)
      user = User(openId=openid,
                  nickName=rData['nickName'],
                  gender = rData['gender'],
                  city = rData['city'],
                  province = rData['province'],
                  country = rData['country'],
                  avatarUrl = rData['avatarUrl'],
                )
      db.session.add(user)
      db.session.commit()

    # 登录用户，并返回由openid和SECRET_KEY构成的token
    login_user(user, True)
    #token = user.generate_auth_token(expiration=expires_in)
    #print('token: %s' % token)
    return jsonify(user.to_dict())

  return str(res)

@auth.route('/secret')
#@login_required
def secret():
  return 'only authenticated users are allowed!'

# 验签数据
import hashlib
def sha1Sign(session_key, rawData):
  data = '%s%s' % (rawData, session_key)
  #a='{"nickName":"Band","gender":1,"language":"zh_CN","city":"Guangzhou","province":"Guangdong","country":"CN","avatarUrl":"http://wx.qlogo.cn/mmopen/vi_32/1vZvI39NWFQ9XM4LtQpFrQJ1xlgZxx3w7bQxKARol6503Iuswjjn6nIGBiaycAjAtpujxyzYsrztuuICqIM5ibXQ/0"}HyVFkGl5F5OQWJZZaNzBBg=='
  #print(hashlib.sha1(a.encode('utf-8')).hexdigest())
  return hashlib.sha1(data.encode('utf-8')).hexdigest()

# 解密加密数据，获取watermark中的appid
import base64
import json
from Crypto.Cipher import AES
def decrypt(session_key, encryptedData, iv):
  sessionKey = base64.b64decode(session_key)
  encryptedData = base64.b64decode(encryptedData)
  iv = base64.b64decode(iv)

  cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
  s = cipher.decrypt(encryptedData)
  decrypted = json.loads(s[:-ord(s[len(s)-1:])])
  print(decrypted)

  return decrypted['watermark']['appid']
