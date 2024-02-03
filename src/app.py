
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/user', methods=['GET'])
def get_all_users():
    allUsers = User.query.all()

    response_body = [user.serialize() for user in allUsers]

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed

logID = 1, 


@app.route('/people', methods=['GET'])
def get_all_characters():

    allCharacters = Character.query.all()

    result = [element.character.serialize() for element in allCharacters]

    return jsonify(result), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):

    character = Character.query.get(people_id)

    result = character.serialize()

    return jsonify(result), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():
    allPlanets = Planet.query.all()

    result = [element.serialize() for element in allPlanets]

    return jsonify(result), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planet.query.get(planet_id)

    result = planet.serialize()

    return jsonify(result), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):

    new_favorite = Favorite(user_id=logID, planet_id=planet_id)

    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        'favorite': new_favorite.serialize()
    }

    return jsonify(response_body), 200


@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):

    new_favorite = Favorite(user_id=logID, character_id=character_id)

    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        'favorite': new_favorite.serialize()
    }

    return jsonify(response_body), 200


@app.route('/user/favorites', methods=['GET'])
def get_all_favorites():

    favorites = Favorite.query.all()

    result = [element.serialize() for element in favorites]

    return jsonify(result), 200


@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(favorite_id):

    favorite = Favorite.query.get(favorite_id)

    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    response_body = {
        "msg": "Favorite character deleted"
    }

    return jsonify(response_body), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(favorite_id):

    favorite = Favorite.query.get(favorite_id)

    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    response_body = {
        "msg": "Favorite planet deleted"
    }

    return jsonify(response_body), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
