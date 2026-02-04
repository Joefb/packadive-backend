from app.models import db, CheckList
from .schemas import checklist_schema, create_checklist_schema
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


# get all check lists for logged in user
@checklist_bp.route("", methods=["GET"])
@auth_token_required
def get_checklists():
    current_user_id = request.logged_in_id
    checklists = db.session.query(CheckList).filter_by(user_id=current_user_id).all()

    if not checklists:
        return jsonify({"message": "No check lists found"}), 404

    return checklist_schema.jsonify(checklists, many=True), 200
