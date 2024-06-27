from init import db, ma
from marshmallow import fields #for the FK

class Comment(db.Model): #child of model class
    __tablename__ = "comments"
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False) #nullable false so it doesn't create an empty comment
    date = db.Column(db.Date) #When was the comment made
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), nullable=False)
    
    user = db.relationship("User", back_populates="comments") #connect to the User module and the comments made by a user
    card = db.relationship("Card", back_populates="comments")
    
    
    #create comment schema
class CommentSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    card = fields.Nested("CardSchema", exclude=["comments"])
    class Meta:
        fields = ("id", "message", "date", "user", "card")
        
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)