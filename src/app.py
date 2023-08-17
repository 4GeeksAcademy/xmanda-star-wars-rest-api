"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET all of the users

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    users_serialized = list(map(lambda x: x.serialize(), users))
    return jsonify({"msg": 'Completed', "users": users_serialized})

#GET single user

@app.route('/user/<int:user_id>', methods=['GET'])
def single_user(user_id):
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        raise APIException('User not found', status_code=404)
    return jsonify(user.serialize()), 200

#GET all of the characters

@app.route('/character', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    characters_serialized = list(map(lambda x: x.serialize(), characters))
    return jsonify({"msg": 'Completed', "characters": characters_serialized})

#GET single character

@app.route('/character/<int:character_id>', methods=['GET'])
def single_character(character_id):
    
    character = Character.query.filter_by(id=character_id).first()
    if character is None:
        raise APIException('Character does not exist', status_code=404)
    return jsonify(character.serialize()), 200

#GET all of the planets

@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify({"msg": 'Completed', "planets": planets_serialized})

#GET single planet

@app.route('/planet/<int:planet_id>', methods=['GET'])
def single_planet(planet_id):
    
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None:
        raise APIException('Planet does not exist', status_code=404)
    return jsonify(planet.serialize()), 200

#Favorites-----------------------------------------------------------

#GET specific user's favorites

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    listfavorites = Favorites.query.filter_by(user_id=user_id).all()
    favorites = list(map(lambda x: x.serialize(),listfavorites))

    return jsonify(favorites), 200


#POST a new favorite character to a user

@app.route('/user/<int:user_id>/favorites/character', methods=['POST'])
def add_character(user_id):
    request_body_favorite = request.get_json()
    favorite_character = Favorites.query.filter_by(user_id=user_id, character_id=request_body_favorite["character_id"]).first()
    if favorite_character is None:
        raise APIException('Please enter a valid character_id', status_code=404)

    newFavoriteCharacter = Favorites(
    user_id=user_id, character_id=request_body_favorite["character_id"])    
    db.session.add(newFavoriteCharacter)
    db.session.commit()
    return jsonify("Character added to favorites"), 200

#POST a new favorite planet to a user

@app.route('/user/<int:user_id>/favorites/planet', methods=['POST'])
def add_planet(user_id):
    request_body_favorite = request.get_json()
    favorite_planet = Favorites.query.filter_by(user_id=user_id, planet_id=request_body_favorite["planet_id"]).first()
    if favorite_planet is None:
        raise APIException('Please enter a valid planet_id', status_code=404)

    newFavoritePlanet = Favorites(
    user_id=user_id, planet_id=request_body_favorite["planet_id"])    
    db.session.add(newFavoritePlanet)
    db.session.commit()
    return jsonify("Planet added to favorites"), 200

#DELETE a favorite character from user
    
@app.route('/user/<int:user_id>/favorites/character/', methods=['DELETE'])
def delete_character(user_id):
    request_body = request.get_json()
    characterToBeDeleted = Favorites.query.filter_by(user_id=user_id, character_id=request_body["character_id"]).first()
    if characterToBeDeleted is None:
        raise APIException("Please select a valid character_id", status_code=404)
    
    db.session.delete(characterToBeDeleted)
    db.session.commit()
    return jsonify("Character was removed from favorites"), 200

#DELETE a favorite planet from user

def delete_planet(user_id):
    request_body = request.get_json()
    planetToBeDeleted = Favorites.query.filter_by(user_id=user_id, planet_id=request_body["planet_id"]).first()
    if planetToBeDeleted is None:
        raise APIException("Please select a valid planet_id", status_code=404)
    
    db.session.delete(planetToBeDeleted)
    db.session.commit()
    return jsonify("Planet was removed from favorites"), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
