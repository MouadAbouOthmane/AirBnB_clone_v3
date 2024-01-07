#!/usr/bin/python3
"""User View"""


from api.v1.views import app_views
from models.user import User
from flask import jsonify, abort, make_response, request
from models import storage
import json


@app_views.route('/users', methods={'GET'}, strict_slashes=False)
def get_users():
    """Retrieves the list of all User"""
    lst = []
    for user in storage.all(User).values():
        lst.append(user.to_dict())
    return jsonify(lst)


@app_views.route('/users/<user_id>', methods={'GET'}, strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    result = storage.get(User, user_id)
    return jsonify(result.to_dict()) if result else abort(404)


@app_views.route('/users/<user_id>',
                 methods={'DELETE'},
                 strict_slashes=False)
def del_user(user_id):
    """Deletes a User object"""
    result = storage.get(User, user_id)
    if result:
        result.delete()
        storage.save()
    return make_response(jsonify({}), 200) if result else abort(404)


@app_views.route('/users', methods={'POST'}, strict_slashes=False)
def create_user():
    """ Create a user"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'email' not in data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in data:
        return make_response(jsonify({'error': 'Missing password'}), 400)

    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods={'PUT'}, strict_slashes=False)
def update_user(user_id):
    """ Update a user"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    # Ignore keys: id, created_at and updated_at
    for key in ['updated_at', 'created_at', 'id', 'email']:
        if key in data:
            del data[key]

    user.__dict__.update(data)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
