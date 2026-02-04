from app.models import db, ListItems
from .schemas import list_item_schema, create_list_item_schema
from app.blueprints.list_item import list_item_bp
from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash

from app.util.auth import (
    encode_auth_token,
    auth_token_required,
    admin_auth_token_required,
)


## list items ROUTES ##


@list_item_bp.route("", methods=["POST"])
@auth_token_required
def create_list_item():
    try:
        data = create_list_item_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_list_item = ListItems(
        item_name=data["item_name"],
        status=data["status"],
        checklist_id=data["checklist_id"],
    )

    db.session.add(new_list_item)
    db.session.commit()

    return list_item_schema.jsonify(new_list_item), 201
