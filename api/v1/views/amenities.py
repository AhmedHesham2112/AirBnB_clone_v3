#!/usr/bin/python3
"""Create a new view for Amenity objects that handles
all default RESTFul API actions"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    dict_ = []
    for val in storage.all(Amenity).values():
        dict_.append(val.to_dict())
    return jsonify(dict_)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    if amenity_id is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    res = request.get_json()
    if type(res) != dict:
        return abort(400, description='Not a JSON')
    if 'name' not in res:
        return abort(400, description='Missing name')
    new_amenity = Amenity(**res)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, description='Not a JSON')
    for key, value in res.items():
        if key not in ["id", "amenity_id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
