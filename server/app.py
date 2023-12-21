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


game_rooms = {}
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
    if game_rooms.get(room) is not None:
        if user not in game_rooms.get(room)["player_order"]:
            game_rooms[room]["player_list"].append({user: []})
            game_rooms[room]["player_order"].append(user)
        else:
            pass
            #RUN SOME FUNCTION OR EMIT ALL GAME DATA ALREADY AVAILABLE FOR USER
    else:
        game_rooms[room] = {
            "id": room,
            "player_list": [{user: []}],
            "table_cards": [],
            "deck": [],
            "last_card_dealt": 0,
            "player_order": [user],
            "current_turn": user,
            "turn_number": 0,
            "player_cards_dealt": False,
            "flop_dealt": False,
            "turn_dealt": False,
            "river_dealt": False
        }  

    print(game_rooms.get(room))
    print("User was added to a room")

@socketio.on('shuffleDeck')
def handle_shuffled_deck(deck_data):
    room = deck_data["room"]
    game = game_rooms.get(room)
    print("shuffling deck")
    game["deck"] = deck_data["deck"]
    print(deck_data["deck"][0])
    socketio.emit('shuffleDeck', deck_data['deck'], room = room)

@socketio.on('start_game')
def handle_game_start(data):
    print("server letting players know game is starting...")
    socketio.emit('starting', data["message"], room = data["room"])

@socketio.on('deal_cards')
def deal_cards(data):
    print("deal cards is running....")
    room = data["room"]
    turn = int(data["turn"])
    # cards = data["cards"]
    game = game_rooms.get(room)
    cards = game["deck"]
    cards_dealt = game["player_cards_dealt"]
    if not cards_dealt:
        for player_dict in game["player_list"]:
            for player in player_dict:
                game["current_turn"] = player
                player_dict[player].append(cards[game["last_card_dealt"]])
                player_dict[player].append(cards[game["last_card_dealt"] + 1])
                socketio.emit("dealing", {"user": player, "cards": player_dict[player]}, room = room)
            game["last_card_dealt"] += 2
        game["last_card_dealt"] += 1
        # game["turn_number"] +=1
        game["player_cards_dealt"] = True
        print(game["player_list"])

@socketio.on("deal_flop")
def deal_flop(data):
    print("dealing the flop...")
    
    room = data["room"]
    turn = int(data["turn"])
    game = game_rooms.get(room)
    cards = game["deck"]
    stored_turn = game["turn_number"]
    cards_dealt = game["flop_dealt"]
    print(f"The incoming number for turn in {turn} and the stored turn is {stored_turn}")
    if not game["flop_dealt"]:
        print("running flop logic....")
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        game["last_card_dealt"] += 1
        # game["turn_number"] += 1
        socketio.emit("dealing_flop", {"table_cards": game["table_cards"]}, room = room)
        game["flop_dealt"] = True

@socketio.on("deal_turn")
def deal_turn(data):
    print("dealing the turn...")
    room = data["room"]
    game = game_rooms.get(room)
    if not game["turn_dealt"]:
        cards = game["deck"]
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        game["last_card_dealt"] += 1
        socketio.emit("dealing_turn", {"table_cards": game["table_cards"]}, room = room)
        game["turn_dealt"] = True

@socketio.on("deal_river")
def deal_river(data):
    print("dealing the river...")
    room = data["room"]
    game = game_rooms.get(room)
    if not game["river_dealt"]:
        cards = game["deck"]
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        socketio.emit("dealing_river", {"table_cards": game["table_cards"]}, room = room)
        game["river_dealt"] = True

# @socketio.on("check_win")
# def check_win(data):
#     room = data["room"]
#     game = game_rooms.get(room)
#     winner = {
#         "winner": {

#         }
#     }
#     for player_obj in game["player_list"]:
#         for player in player_obj:


# def check_for_pairs():
#     pass

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5555)

