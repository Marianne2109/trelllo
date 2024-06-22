from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.card import Card, card_schema, cards_schema

cards_bp =  Blueprint("cards", __name__, url_prefix="/cards")

#Route to create CRUDE operations
# /cards - GET - fetch all cards
# /cards/<id> - GET - fetch a single card
# /cards - POST - create a new card
# /cards/<id> - DELETE - delete a card
# /cards/<id> - PUT, PATCH - edit a card

## /cards - GET - fetch all cards
@cards_bp.route("/")
def get_all_cards():
    #fetch all cards but sorted in descending order
    stmt = db.select(Card).order_by(Card.date.desc())
    cards = db.session.scalars(stmt)
    return cards_schema.dump(cards)

# /cards/<id> - GET - fetch a single card
@cards_bp.route("/<int:card_id>")  # < > creates a dynamic route-this card id is the one determined in the url route
def get_one_card(card_id): #GET the id as a parameter in the function
    stmt = db.select(Card).filter_by(id=card_id) #the id is the column in the database
    card = db.session.scalar(stmt) #when filtering by id it's always link to a single card
    if card: #if card exists 
        return card_schema.dump(card) #shows existing card
    else:    #if card doesn't exist
        return{"error": f"Card with id {card_id} not found"}, 404 #shows message and error 404
    

# /cards - POST - create a new card
@cards_bp.route("/", methods=["POST"])
@jwt_required()
def create_card():
    #get the data from the body of the request
    body_data = request.get_json()
    #create new Card model instance
    card = Card(
        title=body_data.get("title"),
        description=body_data.get("description"),
        date=date.today(),
        status=body_data.get("status"),
        priority=body_data.get("priority"),
        user_id=get_jwt_identity()   #user need to be logged in to create a new card. It needs to provide the token
    )
    
     # add and commit to DB
    db.session.add(card)
    db.session.commit()
    # respond
    return card_schema.dump(card)

# /cards/<id> - DELETE - delete a card
@cards_bp.route("/<int:card_id>", methods=["DELETE"])
@jwt_required() #must be logged in to be able to delete a card, we can also add the condition that the user owns the card or user is admin
def delete_card(card_id):
    #fetch the card from the database
    stmt = db.select(Card).filter_by(id=card_id) #filter by the particular card id
    card = db.session.scalar(stmt)
    #if card exists - then delete
    if card:
        db.session.delete(card)
        db.session.commit()
        return {"message": f"Card '{card.title}' deleted successfully"}
    else: #return error
        return {"error": f"Card with id {card_id} not found"}, 404
    
    # /cards/<id> - PUT, PATCH - edit a card
@cards_bp.route("/<int:card_id>", methods=["PUT", "PATCH"])
def update_card(card_id):
    #get data from body of the request
    body_data = request.get_json()
    #get the card from the database
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    # if card
    if card:
        # update the fields as required
        card.title = body_data.get("title") or card.title
        card.description = body_data.get("description") or card.description
        card.status = body_data.get("status") or card.status
        card.priority = body_data.get("priority") or card.priority
        # commit to the DB
        db.session.commit()
              # return a response
        return card_schema.dump(card)
    # else
    else:
        # return an error
        return {"error": f"Card with id {card_id} not found"}, 404
    
    
