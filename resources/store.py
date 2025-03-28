import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
blp = Blueprint ("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(self, store_id):
        item = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Deleting is not implemented")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return {"stores": list(stores.values())}
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the Store")
        except IntegrityError:
            abort(400, "Store already exists")

   
        return store