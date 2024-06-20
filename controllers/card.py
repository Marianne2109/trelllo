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
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    user = db.relationship('User', back_populates='cards') #Feature of sqlalchemy. We need to match the model name. It connects with the user model. backpopulates is that connects them. User is an object in itself
    
    
class CardSchema(ma.Schema):
    
    user = fields.Nested('UserSchema', only=["id", "name", "email"])
    
    class Meta:
            fields = ( "id", "title", "description", "date", "status", "priority", "user" ) #ma serialize this fields

card_schema = CardSchema()
cards_schema = CardSchema(many=True)