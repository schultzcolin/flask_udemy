from flask.views import MethodView
from flask_smorest import Blueprint, abort 
from passlib.hash import pbkdf2_sha512
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from db import db 
from models import UserModel
from schemas import UserSchema
from blocklist import BLOCKLIST
blp = Blueprint("Users", "user", description="Operations on Users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data['username']).first():
            abort(409, message="A user with that username already exists")

        user = UserModel(
            username = user_data['username'],
            password=pbkdf2_sha512.hash(user_data['password'])

        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created succesfully."}, 201

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out "}

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data['username']
        ).first()

        if user and pbkdf2_sha512.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}
        abort(401, meessage="invalid credentials")

@blp.route("/user/<int:user_id>")
class User(MethodView):


    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200