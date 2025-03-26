import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema
blp = Blueprint ("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")
    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"mesasge": "store deleted."}
        except KeyError:
            abort(404, "Store not found.")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return {"stores": list(stores.values())}
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, request_data):
        for store in stores.values():
            if request_data['name'] == store['name']:
                abort(400, "Store already exists")
        store_id = uuid.uuid4().hex
        new_store = {**request_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201