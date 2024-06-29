from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from init import bcrypt, db
from models.user import User, user_schema, UserSchema

#create instace of the blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

#create routes
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:    #get data from the body of the request
        body_data = UserSchema().load(request.get_json())
        #create an instance of the user module
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email")
        )
        
        #extract tha password from the body
        password=body_data.get("password")
        
        #hash the password
        if password: #if the password exists
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
            
        #add and commit to the DB
        db.session.add(user)
        db.session.commit()
        
        #respond back
        return user_schema.dump(user), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE.VIOLATION:
            return {"error": "Email address already in use"}, 409

@auth_bp.route("/login", methods=["POST"])
def login_user():
    # get the data from the body of the request
    body_data = request.get_json()
    
    # find the user in DB with that email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    #check if user exists and if password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        #create jwt
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        #responde back
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
    #else
    else:
        #respond back with error message
        return {"error": "Invalid email or password"}, 401

    
# /auth/users/user_id
@auth_bp.route("/users", methods=["PUT", "PATCH"])
@jwt_required()
def update_user():
    # get the fields from body of the request
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")
    # fetch the user from the db
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    # if user exists
    if user:
        # update the fields
        user.name = body_data.get("name") or user.name
        # user.password = <hashed-password> or user.password
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # commit to the DB
        db.session.commit()
        # return a response
        return user_schema.dump(user)
    # else
    else:
        # return an error
        return {"error": "User does not exist"}
