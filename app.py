# First lesson on flask api from udemy course I am taking
# basic functionality, we will not be storing our data in memory 
# created on 3/20/25 

from flask import Flask, request
from flask_smorest import abort
from db import items, stores
import uuid

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.post("/store")
def create_store():
    request_data = request.get_json()
    if "name" not in request_data:
        abort(400, message="Bad Request. Ensure the name is included in the json payload")
    for store in stores.values():
        if request_data['name'] == store['name']:
            abort(400, "Store already exists")
    store_id = uuid.uuid4().hex
    new_store = {**request_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201 


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if("price" not in item_data
       or "store_id" not in item_data 
       or "name" not in item_data):
        abort(
            400, message="Bad request. Ensure price, store_id and name are included in the json payload"
        )
    for item in items.values():
        if(item_data["name"] == item["name"]
           and item_data["store_id"] == item["store_id"]
           ):
            abort(400, message="Item already exists")
        
    if item_data['store_id'] not in stores:
        abort(404, message="Store not found.")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201 

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")

@app.get("/item/<string:item_id>")
def get_item(item_id):
   try:
       return items[item_id]
   except KeyError:
       abort(404, "Item not found.")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"mesasge": "Item deleted."}
    except KeyError:
        abort(404, "Item not found.")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure price and name are included in the payload")
    try:
        item = items[item_id]
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")

@app.delete("/item/<string:store_id>")
def delete_store(store_id):
    try:
        del items[store_id]
        return {"mesasge": "store deleted."}
    except KeyError:
        abort(404, "Store not found.")