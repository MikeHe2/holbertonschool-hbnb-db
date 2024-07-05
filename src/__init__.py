""" Initialize the Flask app. """

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os

cors = CORS()
bcrypt = Bcrypt()

def create_app(config_class="src.config.DevelopmentConfig") -> Flask:
    """
    Create a Flask app with the given configuration class.
    The default configuration class is DevelopmentConfig.
    """

    app = Flask(__name__)
    app.url_map.strict_slashes = False


    if os.environ.get("ENV") == "development":
        config_class = "src.config.DevelopmentConfig"
    elif os.environ.get("ENV") == "testing":
        config_class = "src.config.TestingConfig"
    elif os.environ.get("ENV") == "production":
        config_class = "src.config.ProductionConfig"

    app.config.from_object(config_class)

    from flask_jwt_extended import JWTManager

    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
    jwt = JWTManager(app)

    from src.models import db
    db.init_app(app)

    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    print(f"using {config_class} ass config")

    return app


def register_extensions(app: Flask) -> None:
    """Register the extensions for the Flask app"""
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    # Further extensions can be added here


def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""

    # Import the routes here to avoid circular imports
    from src.routes.users import users_bp, auth_bp
    from src.routes.countries import countries_bp
    from src.routes.cities import cities_bp
    from src.routes.places import places_bp
    from src.routes.amenities import amenities_bp
    from src.routes.reviews import reviews_bp

    # Register the blueprints in the app
    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)
    app.register_blueprint(auth_bp)

def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    app.errorhandler(404)(lambda e: (
        {"error": "Not found", "message": str(e)}, 404
    )
    )
    app.errorhandler(400)(
        lambda e: (
            {"error": "Bad request", "message": str(e)}, 400
        )
    )