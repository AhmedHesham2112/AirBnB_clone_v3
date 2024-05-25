#!/usr/bin/python3
"""Create a new view for place objects that handles
all default RESTFul API actions"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = []
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.place_id == place_id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>/', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    if review_id is None:
        abort(404)
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, description="Not a JSON")
    if 'user_id' not in res:
        return abort(400, description="Missing user_id")
    user = storage.get(User, res.user_id)
    if not user:
        abort(404)
    city = storage.get(City, res.city_id)
    if not city:
        abort(404)
    if 'name' not in res:
        return abort(400, description="Missing name")
    new_review = Review(**res)
    new_review.place_id = place.id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, description="Not a JSON")
    for key, value in res.items():
        if key not in ["id", "place_id", "user_id","created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
