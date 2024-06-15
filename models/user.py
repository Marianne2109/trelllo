from init import db, ma

class User(db.Model):
    #name of the table
    __tablename__ = "users"
    
    #attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    

#create schema - the schema can be created in a separate folder
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "is_admin")

#schema to handle a single user objet
user_schema = UserSchema(exclude=["password"])

#schema to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])