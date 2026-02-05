from app.models import db, ListItems, CheckList
from .schemas import list_item_schema
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


# create new item
@list_item_bp.route("", methods=["POST"])
@auth_token_required
def create_list_item():
    try:
        data = list_item_schema.load(request.json)
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


# update list item
@list_item_bp.route("/<int:list_item_id>", methods=["PUT"])
@auth_token_required
def update_list_item(list_item_id):
    try:
        list_item = db.session.get(ListItems, list_item_id)
        print(f"list_item {list_item}")
        if not list_item:
            return jsonify({"message": "Item not found"}), 404

        if list_item.checklist_id is None:
            return jsonify({"message": "Unauthorized"}), 403

        checklist = db.session.get(CheckList, list_item.checklist_id)

        if not checklist or int(checklist.user_id) != int(request.logged_in_id):
            return jsonify({"message": "Unauthorized"}), 403

    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in request.json.items():
        setattr(list_item, key, value)

    db.session.commit()
    return list_item_schema.jsonify(list_item), 200
