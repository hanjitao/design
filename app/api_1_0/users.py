from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import User
from .authentication import auth
from decimal import Decimal

@api.route('/users')
#@auth.login_required
def get_users():
  users = User.query.all()
  return jsonify({'users' : [user.to_json() for user in users]})

@api.route('/users/<int:id>')
def get_user(id):
  user = User.query.get_or_404(id)
  return jsonify(user.to_json())

@api.route('/users', methods=['POST'])
def new_user():
  user = User.from_json(request.json)
  db.session.add(user)
  db.session.commit()
  return jsonify(user.to_json(), 201, {'Location' : url_for('api.get_user', id=user.id, _external=True)})

@api.route('/users/<int:id>', methods=['PUT'])
def edit_user(id):
  user = User.query.get_or_404(id)
  user.name = request.json.get('name', user.name)
  db.session.add(user)
  return jsonify(user.to_json())

@api.route('/users/<int:id>/addCash', methods=['PUT'])
def user_get_ticket(id):
  user = User.query.get_or_404(id)
  user.cashbox += Decimal(request.json.get('cash', '0.0'))
  db.session.add(user)
  db.session.commit()
  return jsonify(user.to_json())

@api.route('/users/<int:id>/subCash', methods=['PUT'])
def user_consume_cashbox(id):
  user = User.query.get_or_404(id)
  user.cashbox -= Decimal(request.json.get('cash', '0.0'))
  db.session.add(user)
  db.session.commit()
  return jsonify(user.to_json())
