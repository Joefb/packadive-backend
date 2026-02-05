from flask import Blueprint

list_item_bp = Blueprint("list_item_bp", __name__)

from . import routes
