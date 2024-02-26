#!/usr/bin/python3
"""Module for state ojects handling RESTFUL API actions """
from flask import jsonify, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """This method retrieves all State objects"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """This method retrieves a State object by id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_state(state_id):
    """This method deletes a State object by id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """This method creates a new State object"""
    new_state = request.get_json()
    if not new_state:
        abort(400, 'Not a JSON')
    if "name" not in new_state:
        abort(400, 'Missing name')

    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """This method updates a State object"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    for key, value in request.get_json().items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
