from app.models import db, User
from .schemas import user_schema, create_user_schema, login_user_schema
from app.blueprints.user import user_bp
from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash

from app.util.auth import (
    encode_auth_token,
    auth_token_required,
)


## USER ROUTES ##
# user login
@user_bp.route("/login", methods=["POST"])
# @limiter.limit("10 per minute")
def user_login():
    try:
        data = login_user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = db.session.query(User).filter_by(user_name=data["user_name"]).first()
    if user and check_password_hash(user.password, data["password"]):
        auth_token = encode_auth_token(user.id)
        return jsonify({"auth_token": auth_token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


# create new user
@user_bp.route("", methods=["POST"])
def create_user():
    try:
        data = create_user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if db.session.query(User).filter_by(user_name=data["user_name"]).first():
        return jsonify({"message": "Username already exists"}), 409

    data["password"] = generate_password_hash(data["password"])
    new_user = User(**data)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201


# delete logged in user
@user_bp.route("", methods=["DELETE"])
@auth_token_required
def delete_logged_in_user():
    current_user_id = request.logged_in_id
    curret_user = db.session.get(User, current_user_id)

    db.session.delete(curret_user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
