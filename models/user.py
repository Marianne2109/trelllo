from init import db, ma
from marshmallow import fields

class User(db.Model):
    #name of the table
    __tablename__ = "users"
    
    #attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    cards = db.relationship("Card", back_populates="user")
    comments = db.relationship("Comment", back_populates="user") #connects with comments card
    
    # {
    #     id: 1,
    #     title: "Card 1",
    #     description: "Card 1 desc",
    #     date: "..",
    #     status: "..",
    #     priority: "..",
    #     user_id: 1,
    #     user: {
    #       id: 1,
    #       name: "User 1",
    #       email: "user1@email.com",
    #   }
    # }

    
    
    

#create schema - the schema can be created in a separate folder
class UserSchema(ma.Schema):
    cards = fields.List(fields.Nested('CardSchema', exclude=["user"]))
    comments = fields.List(fields.Nested('CommentSchema', exclude=["user"])) #List nested because a user can make several comments
    
    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "comments")

#schema to handle a single user objet
user_schema = UserSchema(exclude=["password"])

#schema to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])