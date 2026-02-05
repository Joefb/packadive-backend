# Imports
from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.user import user_bp
from .blueprints.checklist import checklist_bp
from .blueprints.list_item import list_item_bp

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

    # Create prefixed blueprint routes
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(checklist_bp, url_prefix="/checklists")
    app.register_blueprint(list_item_bp, url_prefix="/list_item")
    # app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    # This creates the admin user if it does not exist.
    # This is a hard coded password! Change the admin password after first run!
    with app.app_context():
        from app.models import User
        from werkzeug.security import generate_password_hash

        if not db.session.query(User).filter_by(user_name="admin").first():
            admin_user = User(
                email="admin@admin.com",
                user_name="admin",
                password=generate_password_hash("password"),
            )
            db.session.add(admin_user)
            db.session.commit()

    return app
