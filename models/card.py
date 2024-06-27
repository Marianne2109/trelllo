from init import db, ma
from marshmallow import fields

class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.Date) # Created Date
    status = db.Column(db.String)
    priority = db.Column(db.String)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) #foreing key is a feature provided by the database. user_id is the actual column
    
    user = db.relationship("User", back_populates="cards") #Feature of sqlalchemy. We need to match the model name. It connects with the user model. backpopulates is that connects them. User is an object in itself
    comments = db.relationship("Comment", back_populates="card", cascade="all, delete")

    
class CardSchema(ma.Schema):
    
    user = fields.Nested("UserSchema", only=["id", "name", "email"])
    comments = fields.List(fields.Nested("CommentSchema", exclude=["card"]))
    
    class Meta:
            fields = ( "id", "title", "description", "date", "status", "priority", "user", "comments") #ma serialize this fields
            ordered = True
            
card_schema = CardSchema()
cards_schema = CardSchema(many=True)