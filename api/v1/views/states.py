#!/usr/bin/python3
"""State View"""


from api.v1.views import app_views
from models.state import State
from flask import jsonify, abort, make_response, request
from models import storage
import json


@app_views.route('/states', methods={'GET'}, strict_slashes=False)
def get_states():
    """Retrieves the list of all State"""
    lst = []
    for state in storage.all(State).values():
        lst.append(state.to_dict())
    return jsonify(lst)


@app_views.route('/states/<state_id>', methods={'GET'}, strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    result = storage.get(State, state_id)
    return jsonify(result.to_dict()) if result else abort(404)


@app_views.route('/states/<state_id>',
                 methods={'DELETE'},
                 strict_slashes=False)
def del_state(state_id):
    """Deletes a State object"""
    result = storage.get(State, state_id)
    if result:
        result.delete()
        storage.save()
    return make_response(jsonify({}), 200) if result else abort(404)


@app_views.route('/states', methods={'POST'}, strict_slashes=False)
def create_state():
    """ Create a state"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods={'PUT'}, strict_slashes=False)
def update_state(state_id):
    """ Update a state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    # Ignore keys: id, created_at and updated_at
    for key in ['updated_at', 'created_at', 'id']:
        if key in data:
            del data[key]

    state.__dict__.update(data)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
