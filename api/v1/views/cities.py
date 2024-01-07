#!/usr/bin/python3
"""City View"""


from api.v1.views import app_views
from models.city import City
from models.state import State
from flask import jsonify, abort, make_response, request
from models import storage
import json


@app_views.route('/states/<state_id>/cities',
                 methods={'GET'},
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City"""
    lst = []
    for city in storage.all(City).values():
        if city.state_id == state_id:
            lst.append(city.to_dict())
    return jsonify(lst)


@app_views.route('/cities/<city_id>', methods={'GET'}, strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    result = storage.get(City, city_id)
    return jsonify(result.to_dict()) if result else abort(404)


@app_views.route('/cities/<city_id>',
                 methods={'DELETE'},
                 strict_slashes=False)
def del_city(city_id):
    """Deletes a City object"""
    result = storage.get(City, city_id)
    if result:
        result.delete()
        storage.save()
    return make_response(jsonify({}), 200) if result else abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods={'POST'},
                 strict_slashes=False)
def create_city(state_id):
    """ Create a city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data['state_id'] = state.id
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>',
                 methods={'PUT'},
                 strict_slashes=False)
def update_city(city_id):
    """ Update a state"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    # Ignore keys: id, created_at and updated_at
    for key in ['updated_at', 'created_at', 'id', 'state_id']:
        if key in data:
            del data[key]

    city.__dict__.update(data)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
