#!/usr/bin/python3
"""This module is the amenities module"""

from flask import request, jsonify, abort, make_response

from api.v1.models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Method that retrieves all Amenity objects"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
        strict_slashes=False))
def get_amenity(amenity_id):
    """method that retrieves Amenity object"""
    amenity = storage.all(Amenity).get(f"Amenity.{amenity_id}")
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
        strict_slashes=False))
def delete_amenity(amenity_id):
    """Method that deletes an Amenity object"""
    amenity = storage.all(Amenity).get(f"Amenity.{amenity_id}")
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
        strict_slashes=False)
def create_amenity():
    """Method that creates an Amenity object"""
    json_data = request.get_json()
    if type(json_data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in json_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(name=json_data.get('name'))
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
        strict_slashes=False)
def update_amenity(amenity_id):
    """Method that updates Amenity object"""
    amenity = storage.all(Amenity).get(f"Amenity.{amenity_id}")
    if not amenity:
        abort(404)
    json_data = request.get_json()
    if type(json_data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    allowed_keys = ['name']
    for key, value in json_data.items():
        if key in allowed_keys:
            setattr(amenity, key, values)

       amenity.save()
    return jsonify(amenity.to_dict()), 200
