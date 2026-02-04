import os
from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "3f2b4c6d8e0f1a"


def encode_auth_token(user_id):
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        "iat": datetime.now(timezone.utc),
        "sub": str(user_id),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def auth_token_required(f):
    @wraps(f)
    def decoration(
        *args, **kwargs
    ):  # The function that runs before the functiuon that we're wrapping
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split()[1]

        if not token:
            return jsonify({"error": "token missing from authorization headers"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print(data)
            request.logged_in_id = data["sub"]
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": "token is expired"}), 403
        except jose.exceptions.JWTError:
            return jsonify({"message": "invalid token"}), 401

        return f(*args, **kwargs)

    return decoration


def admin_auth_token_required(f):  # f stands for the function that is getting wrapped
    @wraps(f)
    def decoration(
        *args, **kwargs
    ):  # The function that runs before the functiuon that we're wrapping
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split()[1]

        if not token:
            return jsonify({"error": "token missing from authorization headers"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if data.get("user_name") != "admin":
                return jsonify({"message": "admin access required"}), 403
            print(data)
            request.logged_in_id = data["sub"]
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": "token is expired"}), 403
        except jose.exceptions.JWTError:
            return jsonify({"message": "invalid token"}), 401

        return f(*args, **kwargs)

    return decoration
