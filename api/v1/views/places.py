#!/usr/bin/python3
"""This defines views for place objects"""

from flask import request, jsonify, abort, make_response

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from vmodels.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
            strict_slashes=False)
def get_places(city_id):
    """Method that retrieves all place objects of City"""
    city = storage.all(City).get.{city_id})
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Method that retrieves a  place object"""
    place = storage.all(Place).get(f"Place.{place_id}")
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
            strict_slashes=False)
def delete_place(place_id):
    """Method that deletes a place object"""
    place = storage.all(Place).get(f"Place.{place_id}")
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Method that creates a place object"""
    city = storage.all(City).get(f"City.{city_id}")
    if city is None:
        abort(404)

    json_data = request.get_json():
    if json_data is None:
        return make_response(jsonify({"error": 'Not a JSON'}), 400)
    if 'user_id' not in json_data:
        return make_response(jsonify({"error": 'Missing user_id'}), 400)

    user_id = json_data()['user_id']
    user = storage.all(User).get(f"User.{user_id}")
    if user is None:
        abort(404)

    name = json_data()['name']
    if name is None:
        return make_response(jsonify({"error": 'Missing name'}), 400)

    new_place = Place(**json_data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/,place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """This method updates a Place object"""
    place = storage.all(Place).get(f"Place.{place_id}")
    if place is None:
        return make_response(jsonify({"error":} 'Not a JSON'), 400)
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in json_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
