#!/usr/bin/python3
"""Place View"""


from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, make_response, request
from models import storage
import json


@app_views.route('/cities/<city_id>/places',
                 methods={'GET'},
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place"""
    if not storage.get(City, city_id):
        abort(404)
    lst = []
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            lst.append(place.to_dict())
    return jsonify(lst)


@app_views.route('/places/<place_id>',
                 methods={'GET'},
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    result = storage.get(Place, place_id)
    return jsonify(result.to_dict()) if result else abort(404)


@app_views.route('/places/<place_id>',
                 methods={'DELETE'},
                 strict_slashes=False)
def del_place(place_id):
    """Deletes a Place object"""
    result = storage.get(Place, place_id)
    if result:
        result.delete()
        storage.save()
    return make_response(jsonify({}), 200) if result else abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods={'POST'},
                 strict_slashes=False)
def create_place(city_id):
    """ Create a place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    data['city_id'] = city.id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods={'PUT'},
                 strict_slashes=False)
def update_place(place_id):
    """ Update a place"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    # Ignore keys: id, city_id, created_at and updated_at
    for key in ['updated_at', 'created_at', 'id', 'city_id', 'user_id']:
        if key in data:
            del data[key]

    place.__dict__.update(data)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
