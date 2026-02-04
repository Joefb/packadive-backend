from app.models import db, CheckList
from .schemas import checklist_schema, checklists_schema
from app.blueprints.checklist import checklist_bp
from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash

from app.util.auth import (
    encode_auth_token,
    auth_token_required,
    admin_auth_token_required,
)


## Check List ROUTES ##


# create new check list for current logged in user
@checklist_bp.route("", methods=["POST"])
@auth_token_required
def create_checklist():
    try:
        data = create_checklist_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    current_user_id = request.logged_in_id

    if (
        db.session.query(CheckList)
        .filter_by(checklist_name=data["checklist_name"], user_id=current_user_id)
        .first()
    ):
        return jsonify({"message": "Check list with this name already exists"}), 409

    new_checklist = CheckList(
        checklist_name=data["checklist_name"], user_id=current_user_id
    )

    db.session.add(new_checklist)
    db.session.commit()

    return checklist_schema.jsonify(new_checklist), 201


# get checklist by id for logged in user
# @checklist_bp.route("/<int:checklist_id>", methods=["GET"])
# @auth_token_required
# def get_checklist_by_id():
#     current_user_id = request.logged_in_id


# get all check lists for logged in user
@checklist_bp.route("", methods=["GET"])
@auth_token_required
def get_checklists():
    current_user_id = request.logged_in_id
    checklists = db.session.query(CheckList).filter_by(user_id=current_user_id).all()

    if not checklists:
        return jsonify({"message": "No check lists found"}), 404

    return checklists_schema.jsonify(checklists), 200


# update check list name for logged in user
@checklist_bp.route("/<int:checklist_id>", methods=["PUT"])
@auth_token_required
def update_checklist(checklist_id):
    try:
        data = create_checklist_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    current_user_id = request.logged_in_id

    checklist = (
        db.session.query(CheckList)
        .filter_by(id=checklist_id, user_id=current_user_id)
        .first()
    )

    if not checklist:
        return jsonify({"message": "Check list not found"}), 404

    checklist.checklist_name = data["checklist_name"]
    db.session.commit()

    return checklist_schema.jsonify(checklist), 200


# delete check list for logged in user
@checklist_bp.route("/<int:checklist_id>", methods=["DELETE"])
@auth_token_required
def delete_checklist(checklist_id):
    current_user_id = request.logged_in_id

    checklist = (
        db.session.query(CheckList)
        .filter_by(id=checklist_id, user_id=current_user_id)
        .first()
    )

    if not checklist:
        return jsonify({"message": "Check list not found"}), 404

    db.session.delete(checklist)
    db.session.commit()

    return jsonify({"message": "Check list deleted"}), 200
