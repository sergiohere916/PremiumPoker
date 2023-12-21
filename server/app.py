#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, jsonify, session, render_template, request, redirect
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_restful import Resource
import random
import string
from string import ascii_uppercase

# Local imports
from config import app, db, api
# Add your model imports
from models import Card



# Instantiate Socket Io
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

all_room_codes = []
all_users = []
all_rooms = {"12": [{"Chester": []}]}
turns_and_card_positions = [{"12": [1, 0]}]

# Views go here!

@app.route('/')
def index():
    return '<h1>Poker Server</h1>'


class Cards(Resource):
    def get(self):
        cards = [card.to_dict() for card in Card.query.all()]
        return make_response(cards, 200)

api.add_resource(Cards, "/cards")

class Room_codes(Resource):
    def get(self):
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        # print(code)
        return make_response({"room_code": code}, 200)
    
api.add_resource(Room_codes, "/room_codes")

@socketio.on('connect')
def handle_connect():
    print("Just connected on server side")

@socketio.on('join_room')
def handle_join_room(room_data):
    print("running join room")
    room = room_data['room']
    user = room_data['user']
    join_room(room)
    # all_room_codes.append(room)
    if all_rooms.get(room) is not None :
        # player = "player"
        # number = len(all_rooms[room]) + 1
        # player = player + str(number)
        # all_rooms.get(room).append({player: user})
        all_rooms.get(room).append({user: []})
    else:
        # player = "player1"
        # all_rooms[room] = [{player: user}]
        all_rooms[room] = [{"table": []}, {user: []}]
        turns_and_card_positions.append({room: [0,0]})  


    # all_users.append({user: room})

    # print(all_room_codes)
    # print(all_users)
    print(all_rooms)
    print("User was added to a room")

@socketio.on('shuffleDeck')
def handle_shuffled_deck(deck_data):
    print("shuffling deck")
    print(deck_data["deck"][0])
    socketio.emit('shuffleDeck', deck_data['deck'], room = deck_data["room"])

@socketio.on('start_game')
def handle_game_start(data):
    print("server letting players know game is starting...")
    socketio.emit('starting', data["message"], room = data["room"])

@socketio.on('deal_cards')
def deal_cards(data):
    current_room = data["room"]
    cards = data["cards"]
    last_position = turns_and_card_positions[current_room][1]
    player_list = all_rooms[current_room]
    
    for player_obj in player_list:
        for user_Name in player_obj:
            # game_data["player"] = user_Name
            player_obj[user_Name].append(cards[last_position])
            player_obj[user_Name].append(cards[last_position + 1])
        last_position = last_position + 2
   



if __name__ == '__main__':
    socketio.run(app, debug=True, port=5555)

