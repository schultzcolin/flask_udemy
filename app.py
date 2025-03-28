# First lesson on flask api from udemy course I am taking
# basic functionality, we will not be storing our data in memory 
# created on 3/20/25 

# docker run -dp 5000:5000 -w /app -v "$(PWD):/app" flask-smorest-api
# command lets you run a docker container and have it reload on coe changes 

from db import db
import models
from flask import Flask, request
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
import os
def create_app(db_url=None):
    app = Flask(__name__)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "Stores REST API"
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config['API_VERSION'] = "V1"
    app.config['OPENAPI_URL_PREFIX'] = "/"
    app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
    app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api = Api(app)

    with app.app_context():
     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    return app

