from flask import Blueprint

user_bp = Blueprint("check_list", __name__)

from . import routes
