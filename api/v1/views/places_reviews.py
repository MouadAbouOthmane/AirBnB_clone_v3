#!/usr/bin/python3
"""Place View"""


from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, make_response, request
from models import storage
import json


@app_views.route('/places/<place_id>/reviews',
                 methods={'GET'},
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review"""
    if not storage.get(Place, place_id):
        abort(404)
    lst = []
    for review in storage.all(Review).values():
        if review.place_id == place_id:
            lst.append(review.to_dict())
    return jsonify(lst)


@app_views.route('/reviews/<review_id>',
                 methods={'GET'},
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    result = storage.get(Review, review_id)
    return jsonify(result.to_dict()) if result else abort(404)


@app_views.route('/reviews/<review_id>',
                 methods={'DELETE'},
                 strict_slashes=False)
def del_review(review_id):
    """Deletes a Review object"""
    result = storage.get(Review, review_id)
    if result:
        result.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods={'POST'},
                 strict_slashes=False)
def create_review(place_id):
    """ Create a Review"""
    city = storage.get(Place, place_id)
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

    if 'text' not in data:
        return make_response(jsonify({'error': 'Missing text'}), 400)

    data['place_id'] = place_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods={'PUT'},
                 strict_slashes=False)
def update_review(review_id):
    """ Update a Review"""

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    # Ignore keys: id, place_id, created_at and updated_at
    for key in ['updated_at', 'created_at', 'id', 'place_id', 'user_id']:
        if key in data:
            del data[key]

    review.__dict__.update(data)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
