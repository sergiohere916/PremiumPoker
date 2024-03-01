from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

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
