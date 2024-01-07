#!/usr/bin/python3
"""Amenity View"""


from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, abort, make_response, request
from models import storage
import json


@app_views.route('/amenities', methods={'GET'}, strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity"""
    lst = []
    for amenity in storage.all(Amenity).values():
        lst.append(amenity.to_dict())
    return jsonify(lst)


@app_views.route('/amenities/<amenity_id>',
                 methods={'GET'},
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    result = storage.get(Amenity, amenity_id)
    return jsonify(result.to_dict()) if result else abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods={'DELETE'},
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes a Amenity object"""
    result = storage.get(Amenity, amenity_id)
    if result:
        result.delete()
        storage.save()
    return make_response(jsonify({}), 200) if result else abort(404)


@app_views.route('/amenities', methods={'POST'}, strict_slashes=False)
def create_amenity():
    """ Create a amenity"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods={'PUT'},
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update a amenity"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    # Ignore keys: id, created_at and updated_at
    for key in ['updated_at', 'created_at', 'id']:
        if key in data:
            del data[key]

    amenity.__dict__.update(data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
