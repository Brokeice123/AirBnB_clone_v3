#!/usr/bin/python3
"""A view for city objects handling default RESTful API actions"""

from flask import jsonify, abort, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
        strict_slashes=False)
def get_cities(state_id):
    """Method that retrieves all City objects of a State"""
    state = storage.all(State).get(f"State.{state_id}")
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Method that retrieves a City object"""
    city = storage.all(City).get(f"City.{city_id}")
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Method that deletes a City object"""
    city = storage.all(f"City).{city_id}")
    if not city:
        abort(404)
    city.delete()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
        strict_slashes=False)
def create_city(state_id):
    """Method that creates a new City object"""
    state = storage.all(State).get(f"State.{state_id}")
    if not state:
        abort(404)

    json_data = request.get_json()

    if type(json_data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in json_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_city = City(state_id=state_id, name=json_data.get('name'))
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Method that updates City object"""
    city = storage.get(City).get(f"City.{city_id}")
    if city is None:
        abort(404)

      json_data = request.get_json()
    if type(json_data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    allowed_keys = ['name']

    for key, value in json_data.items():
        if key in allowed_keys:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
