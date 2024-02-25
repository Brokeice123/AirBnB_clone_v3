#!/usr/bin/python3
"""
Defines status endpoint
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {'amenities': Amenity, 'cities': City,
           'places': Place, 'reviews': Review,
           'states': State, 'users': User}


@app_views.route('/status', methods=['GET'])
def status():
    """
    Retrieves the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """
    Retrieves the number of each objects by type
    """
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
