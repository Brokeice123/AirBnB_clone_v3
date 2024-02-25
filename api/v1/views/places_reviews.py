#!/usr/bin/python3
"""Module that defines review objects"""

from flask import request, jsonify, request, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.all(Place).get(f"place.{place_id}")
    if place is None:
        abort(404)

    reviews = []
    return jsonify(review.to_dict() for review in place.reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Method that retrieves all Review objects"""
    review = storage.all(Review).get(f"Review.{review_id}")
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
            strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review =storage.all(Review).get(f"Review.{review_id}")
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
            strict_slashes=False)
def create_review(place_id):
    """Method that creates a review of a place"""
    place = storage.all(Place).get(f"Place.{place_id}")
    if place is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in json_data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user_id = storage.get(json_data['user_id'])
    user = storage.all(User).get(f"User.{user_id}")
    if user is None:
        abort(404)
    if 'text' not in json_data:
        return make_respinse(jsonify({"error": "Missing text"}), 400)

    new_review = Review(place_id=place_id, **data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/api/v1/reviews/<review_id>', methods=['PUT'],
            strict_slashes=False)
def update_review(review_id):
    """Method that updates review of a place"""
    review = storage.all(Review).get(f"Review.{review_id}")
    if review is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in json_data.items():
    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
    for key, value in json_data.items():
        if key not in ignored_keys:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
