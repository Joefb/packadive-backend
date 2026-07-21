from app.models import db, Trip
from .schemas import trip_schema, trips_schema
from app.blueprints.trip import trip_bp
from app.blueprints.checklist.schemas import checklists_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import limiter

from app.util.auth import (
    auth_token_required,
)


## Trip ROUTES ##


# create new trip for current logged in user
@trip_bp.route("", methods=["POST"])
@auth_token_required
@limiter.limit("30 per hour")
def create_trip():
    try:
        data = trip_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    current_user_id = request.logged_in_id

    if (
        db.session.query(Trip)
        .filter_by(trip_name=data["trip_name"], user_id=current_user_id)
        .first()
    ):
        return jsonify({"message": "Trip with this name already exists"}), 409

    new_trip = Trip(trip_name=data["trip_name"], user_id=current_user_id)

    db.session.add(new_trip)
    db.session.commit()

    return trip_schema.jsonify(new_trip), 201


# get all trips for logged in user
@trip_bp.route("", methods=["GET"])
@auth_token_required
@limiter.limit("100 per minute")
def get_trips():
    current_user_id = request.logged_in_id
    trips = db.session.query(Trip).filter_by(user_id=current_user_id).all()

    return trips_schema.jsonify(trips), 200


# update trip name for logged in user
@trip_bp.route("/<int:trip_id>", methods=["PUT"])
@auth_token_required
@limiter.limit("60 per hour")
def update_trip(trip_id):
    try:
        data = trip_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    current_user_id = request.logged_in_id

    trip = (
        db.session.query(Trip)
        .filter_by(id=trip_id, user_id=current_user_id)
        .first()
    )

    if not trip:
        return jsonify({"message": "Trip not found"}), 404

    trip.trip_name = data["trip_name"]
    db.session.commit()

    return trip_schema.jsonify(trip), 200


# delete trip (and its checklists/list items) for logged in user
@trip_bp.route("/<int:trip_id>", methods=["DELETE"])
@auth_token_required
@limiter.limit("30 per hour")
def delete_trip(trip_id):
    current_user_id = request.logged_in_id

    trip = (
        db.session.query(Trip)
        .filter_by(id=trip_id, user_id=current_user_id)
        .first()
    )

    if not trip:
        return jsonify({"message": "Trip not found"}), 404

    db.session.delete(trip)
    db.session.commit()

    return jsonify({"message": "Trip deleted"}), 200


# get all checklists for a trip owned by the logged in user
@trip_bp.route("/<int:trip_id>/checklists", methods=["GET"])
@auth_token_required
@limiter.limit("100 per minute")
def get_trip_checklists(trip_id):
    current_user_id = request.logged_in_id

    trip = (
        db.session.query(Trip)
        .filter_by(id=trip_id, user_id=current_user_id)
        .first()
    )

    if not trip:
        return jsonify({"message": "Trip not found"}), 404

    return checklists_schema.jsonify(trip.checklists), 200
