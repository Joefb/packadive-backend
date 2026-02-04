# Imports
from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.user import user_bp
# from .blueprints.check_list import check_list_bp
# from .blueprints.list_items import list_items_bp

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
    # app.register_blueprint(check_list_bp, url_prefix="/check_list")
    # app.register_blueprint(list_items_bp, url_prefix="/list_items")
    # app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    # This creates the admin user if it does not exist.
    # Needed to create customers and do other admin stuff
    # with app.app_context():
    #     from app.models import Tech
    #     from werkzeug.security import generate_password_hash
    #
    #     # This is a hard coded password! Change the admin password after first run!
    #     if not db.session.query(Tech).filter_by(last_name="admin").first():
    #         admin_tech = Tech(
    #             first_name="admin",
    #             last_name="admin",
    #             position="admin",
    #             phone="000-000-0000",
    #             password=generate_password_hash("password"),
    #         )
    #         db.session.add(admin_tech)
    #         db.session.commit()

    return app
