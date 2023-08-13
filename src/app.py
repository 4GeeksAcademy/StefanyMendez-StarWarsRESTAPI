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
from models import db, User, People, Planets, Vehicles, People_Details, Planets_Details, Vehicles_Details, People_Favorites, Planets_Favorites, Vehicles_Favorites
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


# <-------------------------------Methods User------------------------------->
@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    all_user = list(map(lambda user: user.serialize(), users))

    response_body = {
        "msg": "GET /user response",
        "users": all_user
    }
    return jsonify(response_body), 200

@app.route('/user', methods=['POST'])
def add_user():
    request_body = request.get_json(force=True)
    
    if "email" not in request_body:
        raise APIException('Please enter your email', status_code=404)

    if "password" not in request_body:
        raise APIException('Please enter a password', status_code=404)

    user = User(email=request_body['email'], password=request_body['password'])
    user.save()

    response_body = {
        "msg": "POST /user response",
        "body": request_body
    }

    return jsonify(response_body), 201

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    request_body = request.get_json(force=True)
    user = User.query.get(user_id)

    if user is None:
        raise APIException('User not found', status_code=404)

    if "password" in request_body:
        user.password = request_body['password']

    if "email" in request_body:
        user.email = request_body['email']

    user.update()

    response_body = {
        "msg": "PUT /user response",
        "body": request_body
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    user = User.query.get(user_id)
    people_favorires = People_Favorites.query.filter_by(id_user = user_id)
    planets_favorites = Planets_Favorites. query.filter_by(id_user = user_id)
    vehicles_favorites = Vehicles_Favorites.query.filter_by(id_user = user_id)
    
    all_people = list(map(lambda people: people, people_favorires))
    all_planets = list(map(lambda planet: planet, planets_favorites))
    all_vehicles = list(map(lambda vehicle: vehicle, vehicles_favorites))
    
    if all_people != []:
        people_favorires = all_people[0]
        people_favorires.delete()
        
    if all_planets != []:
        planets_favorites = all_planets[0]
        planets_favorites.delete()
        
    if all_vehicles != []:
        vehicles_favorites = all_vehicles[0]
        vehicles_favorites.delete()
    
    if user is None:
        raise APIException('User not found', status_code=404)

    user.delete()

    reponse_body = {
        "msg": "DELETE /user response",
        "status": "done"
    }
    return jsonify(reponse_body), 200


# <-------------------------------Method GET All Favorites------------------------------->
@app.route('/user/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    people_favorites = People_Favorites.query.filter_by(id_user=user_id)
    all_people_favorites = list(
        map(lambda people: people.serialize(), people_favorites))
    planets_favorites = Planets_Favorites.query.filter_by(id_user=user_id)
    all_planets_favorites = list(
        map(lambda planet: planet.serialize(), planets_favorites))
    vehicles_favorites = Vehicles_Favorites.query.filter_by(id_user=user_id)
    all_vehicles_favorites = list(
        map(lambda vehicle: vehicle.serialize(), vehicles_favorites))

    response_body = {
        "msg": "ok",
        "favorites": {"people": all_people_favorites,
                      "planets": all_planets_favorites,
                      "vehicles": all_vehicles_favorites
                      }
    }
    return jsonify(response_body), 200


# <-------------------------------Methods People------------------------------->
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    all_people = list(map(lambda character: character.serialize(), people))
    response_body = {
        "msg": "GET /people response",
        "users": all_people
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['POST'])
def add_people():
    request_body = request.get_json(force=True)
    if "uid" not in request_body:
        raise APIException('Please enter the uid', status_code=404)

    if "name" not in request_body:
        raise APIException('Please enter the name', status_code=404)

    if "url" not in request_body:
        raise APIException('Please enter the url', status_code=404)

    people = People(
        uid=request_body['uid'],
        name=request_body['name'],
        url=request_body['url']
    )
    people.save()

    response_body = {
        "msg": "POST /people response",
        "body": request_body
    }

    return jsonify(response_body), 201

@app.route('/people/<int:people_uid>', methods=['PUT'])
def update_people(people_uid):
    request_body = request.get_json(force=True)

    people = People.query.filter_by(uid=people_uid)
    all_details = list(map(lambda people: people, people))

    if all_details == []:
        raise APIException('People not found', status_code=404)

    people = all_details[0]

    if "uid" in request_body:
        people.uid = request_body['uid']

    if "name" in request_body:
        people.name = request_body['name']

    if "url" in request_body:
        people.url = request_body['url']

    people.update()

    response_body = {
        "msg": "PUT /people response",
        "body": request_body
    }

    return jsonify(response_body), 200


@app.route('/people/<int:people_uid>', methods=['DELETE'])
def delete_people(people_uid):

    people = People.query.filter_by(uid=people_uid)
    people_details = People_Details.query.filter_by(uid=people_uid)
    people_favorites = People_Favorites.query.filter_by(id_people=people_uid)

    all_people = list(map(lambda people: people, people))
    all_details = list(
        map(lambda people_details: people_details, people_details))
    all_favorites = list(map(lambda favorites: favorites, people_favorites))

    if all_details != []:
        people_details = all_details[0]
        people_details.delete()

    if all_favorites != []:
        people_favorites = all_favorites[0]
        people_favorites.delete()

    if all_people == []:
        raise APIException('People not found', status_code=404)

    people = all_people[0]
    people.delete()

    reponse_body = {
        "msg": "DELETE /people response",
        "status": "done"
    }
    return jsonify(reponse_body), 200


# <-------------------------------Methods People Details------------------------------->
@app.route('/people/<int:people_uid>', methods=['GET'])
def get_people_details(people_uid):
    people = People_Details.query.filter_by(uid=people_uid)
    all_details = list(map(lambda people: people.serialize(), people))

    if all_details == []:
        raise APIException('People details not found ', status_code=404)

    response_body = {
        "msg": "ok",
        "result": all_details
    }
    return jsonify(response_body), 200

@app.route('/people/details', methods=['POST'])
def add_people_details():
    request_body = request.get_json(force=True)

    if "uid" not in request_body:
        raise APIException('Please enter the uid', status_code=404)

    if "homeworld" not in request_body:
        raise APIException('Please enter the homeworld', status_code=404)

    people_details = People_Details(
        uid=request_body['uid'],
        height=request_body['height'],
        mass=request_body['mass'],
        hair_color=request_body['hair_color'],
        skin_color=request_body['skin_color'],
        eye_color=request_body['eye_color'],
        birth_year=request_body['birth_year'],
        gender=request_body['gender'],
        homeworld=request_body['homeworld']
    )
    people_details.save()

    response_body = {
        "msg": "POST /people/details",
        "result": request_body
    }
    return jsonify(response_body), 201

@app.route('/people/details/<int:people_uid>', methods=['PUT'])
def update_people_details(people_uid):
    request_body = request.get_json(force=True)
    people_details = People_Details.query.filter_by(uid=people_uid)
    all_details = list(map(lambda people: people, people_details))

    if all_details == []:
        raise APIException('People details not found ', status_code=404)

    people_details = all_details[0]

    if "uid" in request_body:
        people_details.uid = request_body['uid']

    if "height" in request_body:
        people_details.height = request_body['height']

    if "mass" in request_body:
        people_details.mass = request_body['mass']

    if "hair_color" in request_body:
        people_details.hair_color = request_body['hair_color']

    if "skin_color" in request_body:
        people_details.skin_color = request_body['skin_color']

    if "eye_color" in request_body:
        people_details.eye_color = request_body['eye_color']

    if "birth_year" in request_body:
        people_details.birth_year = request_body['birth_year']

    if "gender" in request_body:
        people_details.gender = request_body['gender']

    if "homeworld" in request_body:
        people_details.homeworld = request_body['homeworld']

    people_details.update()

    response_body = {
        "msg": "PUT /people/details response",
        "body": request_body
    }

    return jsonify(response_body), 200

@app.route('/people/details/<int:people_uid>', methods=['DELETE'])
def delete_people_details(people_uid):
    people_details = People_Details.query.filter_by(uid=people_uid)
    all_details = list(map(lambda people: people, people_details))

    if all_details == []:
        raise APIException('People details not found ', status_code=404)

    people_details = all_details[0]
    people_details.delete()
    reponse_body = {
        "msg": "DELETE /people response",
        "status": "done"
    }
    return jsonify(reponse_body), 200


# <-------------------------------Methods People Favorites------------------------------->
@app.route('/favorites/people/<int:user_id>', methods=['POST'])
def add_favorite_people(user_id):
    request_body = request.get_json(force=True)

    if "id_people" not in request_body:
        raise APIException('Please enter the id_people', status_code=404)

    people_favorites = People_Favorites(
        id_user=user_id,
        id_people=request_body['id_people']
    )

    people_favorites.save()

    response_body = {
        "msg": "POST favorites/people",
        "result": request_body
    }
    return jsonify(response_body), 201

@app.route('/user/<int:user_id>/favorites/people/<int:people_uid>', methods=['DELETE'])
def delete_favorites_people(user_id, people_uid):
    # request_body = request.get_json(force=True)
    people_favorites = People_Favorites.query.filter_by(
        id_user=user_id, id_people=people_uid)
    all_people = list(map(lambda people: people, people_favorites))

    if all_people == []:
        raise APIException('Favorites people not found', status_code=404)

    people_favorites = all_people[0]
    people_favorites.delete()

    reponse_body = {
        "msg": "DELETE /user/favorites/people response",
        "status": "done"
    }
    return jsonify(reponse_body), 200

    # this only runs if `$ python src/app.py` is executed


# <-------------------------------Methods Planets------------------------------->
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda planet: planet.serialize(), planets))
    response_body = {
        "msg": "GET /planets response",
        "users": all_planets
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['POST'])
def add_planets():
    request_body = request.get_json(force=True)

    if "uid" not in request_body:
        raise APIException('Please enter the uid', status_code=404)

    if "name" not in request_body:
        raise APIException('Please enter the name', status_code=404)

    if "url" not in request_body:
        raise APIException('Please enter the url', status_code=404)

    planets = Planets(
        uid=request_body['uid'],
        name=request_body['name'],
        url=request_body['url']
    )
    planets.save()

    response_body = {
        "msg": "POST /planets response",
        "body": request_body
    }

    return jsonify(response_body), 201

@app.route('/planets/<int:planet_uid>', methods=['PUT'])
def update_planets(planet_uid):
    request_body = request.get_json(force=True)
    planet = Planets.query.filter_by(uid=planet_uid)
    all_details = list(map(lambda planet: planet, planet))

    if all_details == []:
        raise APIException('Planet not found', status_code=404)

    planet = all_details[0]

    if "uid" in request_body:
        planet.uid = request_body['uid']

    if "name" in request_body:
        planet.name = request_body['name']

    if "url" in request_body:
        planet.url = request_body['url']

    planet.update()

    response_body = {
        "msg": "PUT /planets response",
        "body": request_body
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_uid>', methods=['DELETE'])
def delete_planets(planet_uid):

    planet = Planets.query.filter_by(uid=planet_uid)
    planet_details = Planets_Details.query.filter_by(uid=planet_uid)
    planet_favorites = Planets_Favorites.query.filter_by(id_planet=planet_uid)
    people = People_Details.query.filter_by(homeworld=planet_uid)
    
    all_planets = list(map(lambda planet: planet, planet))
    all_details = list(
        map(lambda planet_details: planet_details, planet_details))
    all_favorites = list(map(lambda favorites: favorites, planet_favorites))
    all_people = list(map(lambda people: people, people))


    if all_people != []:
        people = all_people[0]
        people.homeworld = None
        people.update()

    if all_details != []:
        planet_details = all_details[0]
        planet_details.delete()

    if all_favorites != []:
        planet_favorites = all_favorites[0]
        planet_favorites.delete()

    if all_planets == []:
        raise APIException('Planet not found', status_code=404)

    planet = all_planets[0]
    planet.delete()

    reponse_body = {
        "msg": "DELETE /planets response",
        "status": "done"
    }
    return jsonify(reponse_body), 200


# <-------------------------------Methods Planets Details------------------------------->
@app.route('/planets/<int:planets_uid>', methods=['GET'])
def get_planets_details(planets_uid):
    planets_details = Planets_Details.query.filter_by(uid=planets_uid)
    all_details = list(map(lambda planet: planet.serialize(), planets_details))

    if all_details == []:
        raise APIException('Planet details not found', status_code=404)

    response_body = {
        "msg": "ok",
        "result": all_details
    }
    return jsonify(response_body), 200

@app.route('/planets/details', methods=['POST'])
def add_planets_details():
    request_body = request.get_json(force=True)

    if "uid" not in request_body:
        raise APIException('Please enter the uid', status_code=404)

    planets_details = Planets_Details(
        uid=request_body['uid'],
        diameter=request_body['diameter'],
        rotation_period=request_body['rotation_period'],
        orbital_period=request_body['orbital_period'],
        gravity=request_body['gravity'],
        population=request_body['population'],
        climate=request_body['climate'],
        terrain=request_body['terrain'],
        surface_water=request_body['surface_water']
    )

    planets_details.save()

    response_body = {
        "msg": "POST /planets/details",
        "result": request_body
    }
    return jsonify(response_body), 201

@app.route('/planets/details/<int:planets_uid>', methods=['PUT'])
def update_planets_details(planets_uid):
    request_body = request.get_json(force=True)
    planet_details = Planets_Details.query.filter_by(uid=planets_uid)
    all_details = list(map(lambda planet: planet, planet_details))

    if all_details == []:
        raise APIException('Planet details not found', status_code=404)

    planet_details = all_details[0]

    if "uid" in request_body:
        planet_details.uid = request_body['uid']

    if "diameter" in request_body:
        planet_details.diameter = request_body['diameter']

    if "rotation_period" in request_body:
        planet_details.rotation_period = request_body['rotation_period']

    if "orbital_period" in request_body:
        planet_details.orbital_period = request_body['orbital_period']

    if "gravity" in request_body:
        planet_details.gravity = request_body['gravity']

    if "population" in request_body:
        planet_details.population = request_body['population']

    if "climate" in request_body:
        planet_details.climate = request_body['climate']

    if "terrain" in request_body:
        planet_details.terrain = request_body['terrain']

    if "surface_water" in request_body:
        planet_details.surface_water = request_body['surface_water']

    planet_details.update()

    response_body = {
        "msg": "PUT /planets/details response",
        "body": request_body
    }

    return jsonify(response_body), 200

@app.route('/planets/details/<int:planets_uid>', methods=['DELETE'])
def delete_planets_details(planets_uid):
    planet_details = Planets_Details.query.filter_by(uid=planets_uid)
    all_details = list(map(lambda planet: planet, planet_details))

    if all_details == []:
        raise APIException('Planet details not found', status_code=404)

    planet_details = all_details[0]

    planet_details.delete()

    reponse_body = {
        "msg": "DELETE /planet/details response",
        "status": "done"
    }
    return jsonify(reponse_body), 200


# <-------------------------------Methods Planets Favorites------------------------------->
@app.route('/favorites/planets/<int:user_id>', methods=['POST'])
def add_favorite_planets(user_id):
    request_body = request.get_json(force=True)

    if "id_planet" not in request_body:
        raise APIException('Please enter the id_planet', status_code=404)

    planet_favorites = Planets_Favorites(
        id_user=user_id,
        id_planet=request_body['id_planet']
    )

    planet_favorites.save()

    response_body = {
        "msg": "POST favorites/planet",
        "result": request_body
    }
    return jsonify(response_body), 201

@app.route('/user/<int:user_id>/favorites/planets/<int:planets_uid>', methods=['DELETE'])
def delete_favorites_planets(user_id, planets_uid):
    planets_favorites = Planets_Favorites.query.filter_by(
    id_user=user_id, id_planet=planets_uid)
    all_planets = list(map(lambda planet: planet, planets_favorites))

    if all_planets == []:
        raise APIException('Favorites planet not found', status_code=404)

    planets_favorites = all_planets[0]
    planets_favorites.delete()

    reponse_body = {
        "msg": "DELETE /user/favorites/planets response",
        "status": "done"
    }
    return jsonify(reponse_body), 200 


# <-------------------------------Methods Vehicles------------------------------->
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    all_vehicles = list(map(lambda vehicle: vehicle.serialize(), vehicles))
    response_body = {
        "msg": "GET /vehicles response",
        "users": all_vehicles
    }
    return jsonify(response_body), 200

@app.route('/vehicles', methods=['POST'])
def add_vehicles():
    request_body = request.get_json(force=True)

    if "uid" not in request_body:
        raise APIException('Please enter the uid', status_code=404)

    if "name" not in request_body:
        raise APIException('Please enter the name', status_code=404)

    if "url" not in request_body:
        raise APIException('Please enter the url', status_code=404)

    vehicle = Vehicles(
        uid=request_body['uid'],
        name=request_body['name'],
        url=request_body['url']
    )

    vehicle.save()

    response_body = {
        "msg": "POST /vehicles response",
        "body": request_body
    }

    return jsonify(response_body), 201

@app.route('/vehicles/<int:vehicle_uid>', methods=['PUT'])
def update_vehicles(vehicle_uid):
    request_body = request.get_json(force=True)
    vehicle = Vehicles.query.filter_by(uid=vehicle_uid)
    all_details = list(map(lambda vehicle: vehicle, vehicle))

    if all_details == []:
        raise APIException('vehicle not found', status_code=404)

    vehicle = all_details[0]

    if "uid" in request_body:
        vehicle.uid = request_body['uid']

    if "name" in request_body:
        vehicle.name = request_body['name']

    if "url" in request_body:
        vehicle.url = request_body['url']

    vehicle.update()

    response_body = {
        "msg": "PUT /vehicles response",
        "body": request_body
    }

    return jsonify(response_body), 200

@app.route('/vehicles/<int:vehicle_uid>', methods=['DELETE'])
def delete_vehicles(vehicle_uid):

    vehicle = Vehicles.query.filter_by(uid=vehicle_uid)
    vehicle_details = Vehicles_Details.query.filter_by(uid=vehicle_uid)
    vehicle_favorites = Vehicles_Favorites.query.filter_by(
        id_vehicle=vehicle_uid)

    all_vehicles = list(map(lambda vehicle: vehicle, vehicle))
    all_details = list(map(lambda vehicle: vehicle, vehicle_details))
    all_favorites = list(map(lambda favorites: favorites, vehicle_favorites))

    if all_details != []:
        vehicle_details = all_details[0]
        vehicle_details.delete()

    if all_favorites != []:
        vehicle_favorites = all_favorites[0]
        vehicle_favorites.delete()

    if all_vehicles == []:
        raise APIException('vehicle not found', status_code=404)

    vehicle = all_vehicles[0]
    vehicle.delete()

    reponse_body = {
        "msg": "DELETE /vehicles response",
        "status": "done"
    }
    return jsonify(reponse_body), 200


# <-------------------------------Methods Vehicles Details------------------------------->
@app.route('/vehicles/<int:vehicles_uid>', methods=['GET'])
def get_vehiccles_details(vehicles_uid):
    vehicles_details = Vehicles_Details.query.filter_by(uid=vehicles_uid)
    all_details = list(
        map(lambda vehicle: vehicle.serialize(), vehicles_details))

    if all_details == []:
        raise APIException('Vehicle details not found', status_code=404)

    response_body = {
        "msg": "ok",
        "result": all_details
    }
    return jsonify(response_body), 200

@app.route('/vehicles/details', methods=['POST'])
def add_vehicles_details():
    request_body = request.get_json(force=True)

    if "uid" not in request_body:
        raise APIException('Please enter the uid', status_code=404)

    vehicle_details = Vehicles_Details(
        uid=request_body['uid'],
        model=request_body['model'],
        vehicle_class=request_body['vehicle_class'],
        manufacturer=request_body['manufacturer'],
        cost_in_credits=request_body['cost_in_credits'],
        length=request_body['length'],
        crew=request_body['crew'],
        passengers=request_body['passengers'],
        max_atmosphering_speed=request_body['max_atmosphering_speed'],
        consumables=request_body['consumables']
    )

    vehicle_details.save()

    response_body = {
        "msg": "POST /vehicle/details",
        "result": request_body
    }
    return jsonify(response_body), 201

@app.route('/vehicles/details/<int:vehicles_uid>', methods=['PUT'])
def update_vehicles_details(vehicles_uid):
    request_body = request.get_json(force=True)
    vehicle_details = Vehicles_Details.query.filter_by(uid=vehicles_uid)
    all_details = list(map(lambda vehicle: vehicle, vehicle_details))

    if all_details == []:
        raise APIException('Vehicles details not found', status_code=404)

    vehicle_details = all_details[0]

    if "uid" in request_body:
        vehicle_details.uid = request_body['uid']

    if "model" in request_body:
        vehicle_details.model = request_body['model']

    if "vehicle_class" in request_body:
        vehicle_details.vehicle_class = request_body['vehicle_class']

    if "manufacturer" in request_body:
        vehicle_details.manufacturer = request_body['manufacturer']

    if "cost_in_credits" in request_body:
        vehicle_details.cost_in_credits = request_body['cost_in_credits']

    if "length" in request_body:
        vehicle_details.length = request_body['length']

    if "crew" in request_body:
        vehicle_details.crew = request_body['crew']

    if "passengers" in request_body:
        vehicle_details.passengers = request_body['passengers']

    if "max_atmosphering_speed" in request_body:
        vehicle_details.max_atmosphering_speed = request_body['max_atmosphering_speed']

    if "consumables" in request_body:
        vehicle_details.consumables = request_body['consumables']

    vehicle_details.update()

    response_body = {
        "msg": "PUT /vehicles/details response",
        "body": request_body
    }

    return jsonify(response_body), 200

@app.route('/vehicles/details/<int:vehicles_uid>', methods=['DELETE'])
def delete_vehicles_details(vehicles_uid):
    vehicle_details = Vehicles_Details.query.filter_by(uid=vehicles_uid)
    all_details = list(map(lambda vehicle: vehicle, vehicle_details))

    if all_details == []:
        raise APIException('Vehicles details not found', status_code=404)

    vehicle_details = all_details[0]

    vehicle_details.delete()

    reponse_body = {
        "msg": "DELETE /vehicle/details response",
        "status": "done"
    }
    return jsonify(reponse_body), 200


# <-------------------------------Methods Vehicles Favorites------------------------------->
@app.route('/favorites/vehicles/<int:user_id>', methods=['POST'])
def add_favorites_vehicles(user_id):
    request_body = request.get_json(force=True)

    if "id_vehicle" not in request_body:
        raise APIException('Please enter the id_vehicle', status_code=404)

    vehicles_favorites = Vehicles_Favorites(
        id_user=user_id,
        id_vehicle=request_body['id_vehicle']
    )

    vehicles_favorites.save()

    response_body = {
        "msg": "POST favorites/people",
        "result": request_body
    }
    return jsonify(response_body), 201

@app.route('/user/<int:user_id>/favorites/vehicles/<int:vehicles_uid>', methods=['DELETE'])
def delete_favorites_vehicles(user_id, vehicles_uid):
    vehicles_favorites = Vehicles_Favorites.query.filter_by(
        id_user=user_id, id_vehicle=vehicles_uid)
    all_vehicles = list(map(lambda vehicle: vehicle, vehicles_favorites))

    if all_vehicles == []:
        raise APIException('Favorites vehicles not found', status_code=404)
    
    vehicles_favorites = all_vehicles[0]
    vehicles_favorites.delete()
    
    reponse_body = {
        "msg": "DELETE /user/favorites/vehicles response",
        "status": "done"
    }
    return jsonify(reponse_body), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
