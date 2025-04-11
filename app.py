# First lesson on flask api from udemy course I am taking
# basic functionality, we will not be storing our data in memory 
# created on 3/20/25 

# docker run -dp 5000:5000 -w /app -v "$(PWD):/app" flask-smorest-api
# command lets you run a docker container and have it reload on coe changes 

from db import db
import models
from flask import Flask, jsonify
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from flask_jwt_extended import JWTManager

from blocklist import BLOCKLIST

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
   # Made with secrets.SystemRandom().getrandbits(128) in the console. 
   # Typically stored in an env variable, not the code. will work on this in the future. 
   app.config["JWT_SECRET_KEY"] = "300341454825717116459708229430908657497"
   jwt = JWTManager(app)





   @jwt.token_in_blocklist_loader
   def check_if_token_in_blocklist(jwt_header, jwt_payload):
      return jwt_payload["jti"] in BLOCKLIST


   @jwt.revoked_token_loader
   def revoked_token_callback(jwt_header, jwt_payload):
      return (
         jsonify(
               {"description": "The token has been revoked.", "error": "token_revoked"}
         ),
         401,
      )

   @jwt.additional_claims_loader
   def add_claims_to_jwt(identity):
      if identity == 1:
         return {"is_admin": True}
      else: 
         return {"is_admin": False}

   @jwt.expired_token_loader
   def experied_token_callback(jwt_header, jwt_payload):
      return (
         jsonify({"message": "the token has expired.", "error": "token_expired"}), 401
      )
   
   @jwt.invalid_token_loader
   def invalid_token_callback(error):
      return{
         jsonify({"message": "signature verification failed", "error": "invalid_token"}), 
         401
      }

   @jwt.unauthorized_loader
   def missing_token_callback(error):
      return(
         jsonify({'description': "Request does not contain an access token", "error": "authorization_required"}), 401
      )
   with app.app_context():
      db.create_all()

   api.register_blueprint(ItemBlueprint)
   api.register_blueprint(StoreBlueprint)
   api.register_blueprint(TagBlueprint)
   api.register_blueprint(UserBlueprint)
   return app

