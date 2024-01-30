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
from models import db, User, People, Planets, FavPlanets, FavPeople

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

#Show all users
@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    response_body = list(map(lambda x: x.serialize(), users))
    return jsonify(response_body), 200

#Show one user
@app.route('/user/<int:userid>', methods=['GET'])
def get_one_user(userid):
    user = User.query.get(userid)
    if user is None:
        return {"message": "User not found"}, 404
    response_body = user.serialize()
    return jsonify(response_body), 200

#Show all characters
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    response_body = list(map(lambda x: x.serialize(), people))
    return jsonify(response_body), 200

#Show one character
@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    one_people = People.query.get(people_id)
    if one_people is None:
        return {"message": "People not found"}, 404
    response_body = one_people.serialize()
    return jsonify(response_body), 200

#Show all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    response_body = list(map(lambda x: x.serialize(), planets))
    return jsonify(response_body), 200

#Show one planet
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):
    one_planet = Planets.query.get(planets_id)
    if one_planet is None:
        return {"message": "Planet not found"}, 404
    response_body = one_planet.serialize()
    return jsonify(response_body), 200

############## FAVORITE PLANETS ##############
#Show all users favorite planets 
@app.route('/user/favorites/planets', methods=['GET'])
def get_all_favplanets():
    favorites = FavPlanets.query.all()
    if favorites is None:
        return {"message": "Data not found"}, 404
    response_body = list(map(lambda x: x.serialize(), favorites))
    if len(response_body) == 0:
        response_body= {"message": "User without favorite planets"}
    return jsonify(response_body), 200

#Show one user favorite planets 
@app.route('/user/<int:userid>/planets', methods=['GET'])
def get_user_favplanets(userid):
    favorites = FavPlanets.query.filter_by(user_id=userid)
    if favorites is None:
        return {"message": "User not found"}, 404
    response_body = list(map(lambda x: x.serialize(), favorites))
    if len(response_body) == 0:
        response_body= {"message": "User without favorite planets"}
    return jsonify(response_body), 200

#Add favorite planet to user with the planet id
@app.route('/user/<int:user_id>/planet/<int:planet_id>', methods=['GET', 'POST'])
def post_fav_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if user is None:
        return {"message": "User not found"}, 404
    planet = Planets.query.get(planet_id)
    if planet is None:
        return {"message": "Planet not found"}, 404
    favorites = FavPlanets.query.filter_by(user_id=user_id, planet_id=planet_id)
    if favorites is not None:
        return {"message": "Favorite planet already exists"}, 200
    new_favplanet = FavPlanets()
    new_favplanet.planet_id = planet_id
    new_favplanet.user_id = user_id
    db.session.add(new_favplanet)
    db.session.commit()
    return get_user_favplanets(user_id)

#Delete favorite planet from user 
@app.route('/user/<int:userid>/planet/delete=<int:planetid>', methods=['GET', 'DELETE'])
def delete_fav_planet(userid, planetid):
    favorites = FavPlanets.query.filter_by(user_id=userid, planet_id=planetid).first()
    if favorites is None:
        return {"message": "Data not found"}, 404
    db.session.delete(favorites)
    db.session.commit()
    return get_user_favplanets(userid)

############## FAVORITE PEOPLE ##############
#Show all users favorite people 
@app.route('/user/favorites/people', methods=['GET'])
def get_all_favpeople():
    favorites = FavPeople.query.all()
    if favorites is None:
        return {"message": "Data not found"}, 404
    response_body = list(map(lambda x: x.serialize(), favorites))
    if len(response_body) == 0:
        response_body= {"message": "User without favorite people"}
    return jsonify(response_body), 200

#Show one user favorite people 
@app.route('/user/<int:userid>/people', methods=['GET'])
def get_user_favpeople(userid):
    favorites = FavPeople.query.filter_by(user_id=userid)
    if favorites is None:
        return {"message": "User not found"}, 404
    response_body = list(map(lambda x: x.serialize(), favorites))
    if len(response_body) == 0:
        response_body= {"message": "User without favorite people"}
    return jsonify(response_body), 200

#Add favorite people to user with the people id
@app.route('/user/<int:user_id>/people/<int:people_id>', methods=['GET', 'POST'])
def post_fav_people(user_id, people_id):
    user = User.query.get(user_id)
    if user is None:
        return {"message": "User not found"}, 404
    people = Planets.query.get(people_id)
    if people is None:
        return {"message": "People not found"}, 404
    favorites = FavPeople.query.filter_by(user_id=user_id, people_id=people_id)
    if favorites is not None:
        return {"message": "Favorite people already exists"}, 200
    new_favpeople = FavPeople()
    new_favpeople.people_id = people_id
    new_favpeople.user_id = user_id
    db.session.add(new_favpeople)
    db.session.commit()
    return get_user_favpeople(user_id)

#Delete favorite people from user 
@app.route('/user/<int:userid>/people/delete=<int:peopleid>', methods=['GET', 'DELETE'])
def delete_fav_people(userid, peopleid):
    favorites = FavPeople.query.filter_by(user_id=userid, people_id=peopleid).first()
    if favorites is None:
        return {"message": "Data not found"}, 404
    db.session.delete(favorites)
    db.session.commit()
    return get_user_favpeople(userid)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)