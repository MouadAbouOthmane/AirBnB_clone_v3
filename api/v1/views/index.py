#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def status():
    """status function return 200"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type:"""
    classes = {'amenities': Amenity, 'cities': City,
               'places': Place, 'reviews': Review,
               'states': State, 'users': User}
    res = {}
    for cls in classes:
        res[cls] = storage.count(classes[cls])
    return jsonify(res)
