from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    birth_year = db.Column(db.Integer, unique=False)
    height = db.Column(db.Integer, unique=False)
    eye_color = db.Column(db.String, unique=False)
    skin_color=db.Column(db.String, unique=False)

    def __repr__(self):
        return f"This is {self.name} with ID {self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "height": self.height,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
    }
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    diameter = db.Column(db.Integer, unique=False)
    climate = db.Column(db.String, unique=False)
    terrain = db.Column(db.String, unique=False)
    orbital_period=db.Column(db.Integer, unique=False)

    def __repr__(self):
        return f"This is planet {self.name} with ID {self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
            "orbital_period": self.orbital_period,
    }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))


    def __repr__(self):
        return f"This is are {self.user_id} favorite characters and planets"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            
    }
