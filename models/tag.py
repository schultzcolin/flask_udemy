from db import db 


class TagModel(db.Model): 
    __tabename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populate="tags", secondary="items_tags")