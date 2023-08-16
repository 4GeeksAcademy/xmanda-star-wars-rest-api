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
def handle_favorites(user_id):
    allfavorites = Favorites.query.filter_by(user_id=user_id).all()
    favoritesList = list(map(lambda fav: fav.serialize(),allfavorites))

    return jsonify(favoritesList), 200

#POST a new favorite character to a user

#@app.route('/user/<int:user_id>/favorites', methods=['POST'])


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
