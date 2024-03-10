from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

# Models go here!
class Card(db.Model, SerializerMixin):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    suit = db.Column(db.String)
    value = db.Column(db.Integer)
    # This is the image column
    image = db.Column(db.String)

    def __repr__(self):
        return f'<Card: {self.name}, suit: {self.suit}, id: {self.id}>'

class Icon(db.Model, SerializerMixin):
    __tablename__ = "icons"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    content = db.Column(db.String)
    price = db.Column(db.Integer)

class Tag(db.Model, SerializerMixin):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    user_id = db.Column(db.String)
    points = db.Column(db.Integer)
    total_points = db.Column(db.Integer)

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be visible")
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))
    

    def to_dict(self):
        return {
            "id" : self.id,
            "username" : self.username
        }

    
    
