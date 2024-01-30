from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=True)
    #planets_fav = db.Column(db.Integer, unique=True, nullable=True)
    #planets_fav = db.Column(db.String(250), unique=True, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.usernamE

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    uid= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(120), unique=False, nullable=False)
    url= db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "url": self.url
        }

class Planets(db.Model):
    uid= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(120), unique=False, nullable=False)
    url= db.Column(db.String(120), unique=True, nullable=False)
    #users_fav = db.Column(db.Integer, unique=True, nullable=True)
    #favorites = db.relationship('Favorites', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "url": self.url,
        }
    
class FavPlanets(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, unique=False, nullable=False)
    planet_id= db.Column(db.Integer, unique=False, nullable=False)
    #planet_id= db.Column(db.Integer, db.ForeignKey('planets.uid'), unique=False, nullable=False)
    #user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return '<FavPlanets %r>' % self.planet_id
    def serialize(self):
        return {
            "user_id" : self.user_id,
            "planet_id" : self.planet_id
        }
    
class FavPeople(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, unique=False, nullable=False)   
    people_id= db.Column(db.Integer, unique=False, nullable=False) 

    def __repr__(self):
        return '<FavPeople %r>' % self.people_id
    def serialize(self):
        return {
            "user_id" : self.user_id,
            "people_id" : self.people_id
        }