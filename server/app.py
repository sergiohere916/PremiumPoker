#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, jsonify, session
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import Card

# Views go here!
class Cards(Resource):
    def get(self):
        cards = [card.to_dict() for card in Card.query.all()]
        return make_response(cards, 200)

api.add_resource(Cards, "/cards")

@app.route('/')
def index():
    return '<h1>Poker Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

