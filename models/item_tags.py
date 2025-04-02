from db import db

class ItemTags(db.Model):
    __tablename__ = "item_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForiegnKey("items.id"))
    tag_id = db.column(db.Integer, db.ForeignKey("tags.id"))