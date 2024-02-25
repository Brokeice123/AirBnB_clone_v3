#!/usr/bin/python3
"""This is the Users Module class"""
from flask import request, make_response, jsonify
from api.v1.models import User
from api.v1.storage import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """This method retrieves all User objects"""
    for user in storage.all("User").values():
        users = storage.all(User)
        return jsonify([user.to_dict() for user in users]), 200


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """This  method retrieves a User object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('users/<string:user_id>', methods=['DELETE'],
                strict_slashes=False)
def delete_user(user_id):
    """This method deletes a user based on its user_id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/<string:user_id>', methods=['POST'],
        strict_slashes=False)
def post_user():
    """This method """
json_data = request.get_json()
    if type(json_data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in json_data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in json_data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """This method updates a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    json_data = request.get_json()
    if type(json_data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in json_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
