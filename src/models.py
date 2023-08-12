from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=True)

    def __repr__(self):
        return '<User %r>' % self.email
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def get_people_favorites(self):
        return list(map(lambda people: people.serialize(), self.people))
        
    def get_planets_favorites(self):
        return list(map(lambda planets: planets.serialize(), self.planets))
        
    def get_vehicles_favorites(self):
        return list(map(lambda vehicles: vehicles.serialize(), self.vehicles))
        
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
        
class Planets (db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique = True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    url = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def serialize(self):
        return{
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "url": self.url
        }
    
class Planets_Details(db.Model):
    __tablename__ = 'planets_details'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('planets.uid'), nullable=False, unique=True)
    diameter = db.Column(db.Integer, nullable=True)
    rotation_period = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    gravity = db.Column(db.String(50), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    climate= db.Column(db.String(100), nullable=True)
    terrain = db.Column(db.String(100), nullable=True)
    surface_water = db.Column(db.Integer, nullable=True)
    planet = db.relationship(Planets)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
        return{
            "id": self.id,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }    
        
class Planets_Favorites(db.Model):
    __tablename__ = 'planet_favorites'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_planet = db.Column(db.Integer, db.ForeignKey('planets.uid'), nullable=False)
    user = db.relationship(User)
    planet = db.relationship(Planets)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
        return{
            "id_planet": self.id_planet
        }
    
class People (db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique = True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    url = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return '<People %r>' % self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
        return{
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "url": self.url
         }
    
class People_Details(db.Model):
    __tablename__ = 'people_details'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('people.uid'), nullable=False, unique=True)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(50))
    skin_color= db.Column(db.String(50))
    eye_color= db.Column(db.String(50))
    birth_year = db.Column(db.String(30))
    gender = db.Column(db.String(30))
    homeworld = db.Column(db.Integer, db.ForeignKey('planets.uid'))
    planet = db.relationship(Planets)
    people = db.relationship(People)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def serialize(self):
        return{
            "id": self.id,
            "uid":self.uid, 
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld
        }
    
class People_Favorites(db.Model):
    __tablename__ = 'people_favorites'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_people = db.Column(db.Integer, db.ForeignKey('people.uid'), nullable=False)
    user = db.relationship(User)
    people = db.relationship(People)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
        return{
            "id_people": self.id_people
        }
    
class Vehicles (db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique = True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    url = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Vehicle %r>' % self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
        return{
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "url": self.url
        }
    
class Vehicles_Details(db.Model):
    __tablename__ = 'vehicles_details'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('vehicles.uid'), nullable=False, unique=True)
    model = db.Column(db.String(50), nullable=True)
    vehicle_class = db.Column(db.String(50), nullable=True)
    manufacturer= db.Column(db.String(50), nullable=True)
    cost_in_credits = db.Column(db.Integer, nullable=True)
    length = db.Column(db.Float, nullable=True)
    crew = db.Column(db.Integer, nullable=True)
    passengers = db.Column(db.Integer, nullable=True)
    max_atmosphering_speed = db.Column(db.Integer, nullable=True)
    consumables = db.Column(db.String(30), nullable=True)
    vehicle = db.relationship(Vehicles)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def serialize(self):
        return{
            "id": self.id,
            "uid":self.uid, 
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "consumables": self.consumables
        }
    
class Vehicles_Favorites(db.Model):
    __tablename__ = 'vehicles_favorites'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_vehicle = db.Column(db.Integer, db.ForeignKey('vehicles.uid'), nullable=False)
    user = db.relationship(User)
    vehicles = db.relationship(Vehicles)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
        return{
            "id_vehicle": self.id_vehicle
        }