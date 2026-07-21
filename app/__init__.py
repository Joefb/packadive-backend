# Imports
import os
from flask import Flask
from .models import db
from .extensions import ma, limiter, cache, migrate
from .blueprints.user import user_bp
from .blueprints.checklist import checklist_bp
from .blueprints.list_item import list_item_bp
from .blueprints.trip import trip_bp
from flask_cors import CORS

## Swagger Setup
# from flask_swagger_ui import get_swaggerui_blueprint
# SWAGGER_URL = "/api/docs"  # URL for exposing my swagger ui
# API_URL = "/static/swagger.yaml"
#
# # creating swagger blueprint
# swagger_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL, API_URL, config={"app_name": "Autos R Us API"}
# )


# Create Flask application instance
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")

    # Init the extension onto the Flask app
    db.init_app(app)  # This adds the db to the app.
    ma.init_app(app)  # This adds Marshmallow to the app.
    limiter.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    # Scope CORS to only allow requests from the specified origins.
    # CORS_ORIGINS overrides this (comma-separated) for local/dev use against
    # a frontend dev server running on a non-prod origin; unset in prod.
    cors_origins_env = os.environ.get("CORS_ORIGINS")
    if cors_origins_env:
        cors_origins = [origin.strip() for origin in cors_origins_env.split(",")]
    else:
        cors_origins = ["https://www.packadive.com", "https://packadive.com"]
    CORS(app, origins=cors_origins)

    # Create prefixed blueprint routes
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(checklist_bp, url_prefix="/checklists")
    app.register_blueprint(list_item_bp, url_prefix="/list_item")
    app.register_blueprint(trip_bp, url_prefix="/trips")
    # app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    # This creates the admin user if it does not exist.
    # This is a hard coded password! Change the admin password after first run!
    # with app.app_context():
    #     from app.models import User
    #     from werkzeug.security import generate_password_hash
    #
    #     if not db.session.query(User).filter_by(user_name="admin").first():
    #         admin_user = User(
    #             email="admin@admin.com",
    #             user_name="admin",
    #             password=generate_password_hash("password"),
    #         )
    #         db.session.add(admin_user)
    #         db.session.commit()

    return app
