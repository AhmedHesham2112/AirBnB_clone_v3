#!/usr/bin/python3
"""Create a new view for Place objects that handles
all default RESTFul API actions"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    state = storage.get('City', city_id)
    if state is None:
        abort(404)
    cities_list = []
    cities = storage.all(City).values()
    for city in cities:
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places', methods=['POST'],
                 strict_slashes=False)
def post_place():
    res = request.get_json()
    if type(res) != dict:
        return abort(400, description='Not a JSON')
    if 'name' not in res:
        return abort(400, description='Missing name')
    if 'user_id' not in res:
        return abort(400, description='Missing user_id')
    user = storage.get('User', request.json()['user_id'])
    if not user:
        abort(404)
    new_place = Place(**res)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, description='Not a JSON')
    for key, value in res.items():
        if key not in ["id", "place_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
