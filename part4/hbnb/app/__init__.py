from flask import Flask, request, make_response
from flask_restx import Api
from app.extensions import bcrypt, db
from flask_jwt_extended import JWTManager
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from flask_cors import CORS
import config

jwt = JWTManager()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    # Configuration CORS simplifiée - UN SEUL endroit
    CORS(
        app,
        resources={r"/api/*": {
            "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }}
    )

    # SUPPRIMEZ la fonction @app.after_request !!!

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app