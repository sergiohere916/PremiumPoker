#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, jsonify, session, render_template, request, redirect
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_restful import Resource
import random
import string
from string import ascii_uppercase
from itertools import combinations
import time
import uuid
import threading

# Local imports
from config import app, db, api
# Add your model imports
from models import Card


# Instantiate Socket Io
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")


game_rooms = {}
players_in_games = {}
turns_and_card_positions = [{"12": [1, 0]}]
#UP TO DATE BACKEND
# Views go here!

#RETURN POINT 2/29/2024
    #HERE
@app.route('/')
def index():
    return '<h1>Poker Server</h1>'

class StoreRoomData(Resource):
    def post(self):
        user = request.json["user"]
        code = request.json["room"]
        uid = request.json["userId"]
        session["user"] = user
        session["room"] = code
        session["userId"] = uid

        print("stored data")
        return {"user": user, "room": code, "userId": uid }, 200
    
api.add_resource(StoreRoomData, "/storeData")

class CheckSession(Resource):
    def get(self):
        print("checking session")
        user = session["user"]
        print("still good...")
        code = session["room"]
        print("got the code now \n")
        uid = session["userId"]
        print("likely breaks here...")
        print("checking session")
        print("user id is: " + uid)
        if user and code and uid:
            return {"user": user, "room": code, "userId": uid}, 200
api.add_resource(CheckSession, "/checkSession")

class Cards(Resource):
    def get(self):
        cards = [card.to_dict() for card in Card.query.all()]
        return make_response(cards, 200)

api.add_resource(Cards, "/cards")

class Room_codes(Resource):
    def get(self):
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        # print(code)
        if code:
            return make_response({"room_code": code}, 200)
        else:
            return make_response({"error": "Failed to generate a room code"}, 500)
    
api.add_resource(Room_codes, "/room_codes")

class Player_ids(Resource):
    def get(self):
        random_id = uuid.uuid1()
        if random_id:
            return make_response({"user_id": random_id}, 200)
        else:
            return make_response({"error": "Failed to generate unique id"}, 500)
    
api.add_resource(Player_ids, "/player_ids")

@socketio.on('connect')
def handle_connect(socket):
    sid = request.sid
    print(f"{sid} Just connected on server side")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    print(f"{sid} disconnected")
    # if players_in_games.get(sid, None):
    #     print("player was in game so need place player in watch list and switch game hosts...")
    #     game = players_in_games[sid][0]
    #     user = players_in_games[sid][1]
    #     #Let the game know this player disconnected add their name to a list to keep track of them
    #     game["disconnected_players"].append(user)
    #     #can possibly check if all possible players are disconnected
    #     if game["host"] == user and game["disconnected_players"] != len:
    #         for player in game["player_order"]:
    #             if player not in game["disconnected_players"]



@socketio.on('left_room')
def handle_leaving_room(room_data):
    print(room_data["user"] + " has left the room")

@socketio.on('join_room')
def handle_join_room(room_data):
    print("\nrunning join room")
    room = room_data['room']
    user = room_data['user']
    userId = room_data["userId"]

    join_room(room)
    if game_rooms.get(room) is not None:
        #game room exists....
        #Added 3/4
        game = game_rooms[room]
        #old model before 2/28 ---------------
        if userId not in game["player_ids"] and len(game["player_ids"]) < 6 and not game["game_started"]:
            #THIS RUNS IF GAME EXISTS AND NEW PLAYER JOINING AND IS NOT FULL OF PLAYERS....maybe add if not game started....
            #Maybe add one more condition to ensure game hasn't started and handle other conditions elsewhere...
            #Look through game for available player seats, if seat is available user is assigned this player/seat ----

            # game = game_rooms[room]
            player_data = game["player_data"]
            if player_data["player1"]["userId"] == "":
                #add the player here
                print("new player has joined the room")
                player_data["player1"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 2000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                game["player_order"].append("player1")
                game["player_map"][userId] = "player1"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"], "ids": game["player_ids"]}, room = room )
                
            elif player_data["player2"]["userId"] == "":
                print("new player has joined the room")
                player_data["player2"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 3000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid, "image": "https://static1.cbrimages.com/wordpress/wp-content/uploads/2019/09/One-Piece-Monkey-D.-Luffy-Cropped.jpg"}
                game["player_ids"].append(userId)
                game["player_order"].append("player2")
                game["player_map"][userId] = "player2"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"], "ids": game["player_ids"]}, room = room )
                
            elif player_data["player3"]["userId"] == "":
                print("new player has joined the room")
                player_data["player3"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 2000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                game["player_order"].append("player3")
                game["player_map"][userId] = "player3"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"], "ids": game["player_ids"]}, room = room )
                
            elif player_data["player4"]["userId"] == "":
                print("new player has joined the room")
                player_data["player4"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 2000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                game["player_order"].append("player4")
                game["player_map"][userId] = "player4"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"], "ids": game["player_ids"]}, room = room )
                
            elif player_data["player5"]["userId"] == "":
                print("new player has joined the room")
                player_data["player5"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 2000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                game["player_order"].append("player5")
                game["player_map"][userId] = "player5"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"], "ids": game["player_ids"]}, room = room )

            elif player_data["player6"]["userId"] == "":
                print("new player has joined the room")
                player_data["player6"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 2000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                game["player_order"].append("player6")
                game["player_map"][userId] = "player6"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"], "ids": game["player_ids"]}, room = room )

        else:
            #IF GAME EXISTS AND PLAYER IS IN THE LIST OF IDS THEY CAN JUST REJOIN IF IN SAME ROUND
            print(f"{user} is rejoining...")
            game = game_rooms[room]
            
            round = game["betting_round"]
            print(f"The round is {round}")
            print(game[round + "_bets_taken"])

            player = game["player_map"][userId]
            player_cards = game["player_data"][player]["cards"]
            player_money = game["player_data"][player]["cash"]

            min_bet_difference = game["min_bet"] - game["player_data"][player][round]
            #ALLOW PLAYER TO REJOIN TO THEIR PROPER STAGE WITHIN THE GAME
            #MAY WANT TO SET GAME TO FALSE AT START ON BACKEND THEN WITH STARTING SET TO TRUE
            if game["game_started"] and game["player_cards_dealt"] == False:
                print("player will be returned to game with their data recovered")
                socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )

            elif game["pregame_bets_taken"] == True and game["pregame_bets_completed"] == False:
                if game["round_order"][game["current_turn"]] == player:
                    print(f"letting {user} bet again")
                    socketio.emit('rejoin_at_bet',{"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room)
                else:
                    print("player will be returned to game with their data recovered")
                    socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            
            elif game["game_started"] and game["flop_dealt"] == False:
                print("player will be returned to game with their data recovered")
                socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            
            elif game["pregame_bets_completed"] and game["flop_bets_taken"] and game["flop_bets_completed"] == False:
                if game["round_order"][game["current_turn"]] == player:
                    print(f"letting {user} bet again")
                    socketio.emit('rejoin_at_bet',{"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room)
                else:
                    print("player will be returned to the flop betting with their data recovered, but it is not yet their turn")
                    socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            
            elif game["game_started"] and game["turn_dealt"] == False:
                print("player will be returned to game with their data recovered")
                socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            
            elif game["flop_bets_completed"] and game["turn_bets_taken"] and game["turn_bets_completed"] == False:
                if game["round_order"][game["current_turn"]] == player:
                    print(f"letting {user} bet again")
                    print(game["all_player_cards"])
                    socketio.emit('rejoin_at_bet',{"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room)
                else:
                    print("player will be returned to the flop betting with their data recovered, but it is not yet their turn")
                    socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            
            elif game["game_started"] and game["river_dealt"] == False:
                print("player will be returned to game with their data recovered")
                print("river cards should be dealt out directly after?")
                socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            
            elif game["turn_bets_completed"] and game["river_bets_taken"] and game["river_bets_completed"] == False:
                if game["round_order"][game["current_turn"]] == player:
                    print(f"letting {user} bet again")
                    print(game["all_player_cards"])
                    socketio.emit('rejoin_at_bet',{"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room)
                else:
                    print("player will be returned to the flop betting with their data recovered, but it is not yet their turn")
                    socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            else:
                #TRYING TO IMPLEMENT THIS AS RETURNING AT ANY OTHER POINT
                print(f"player: {user} will be returned to the flop betting with their data recovered, but just standard in between actions..")
                socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
    else:
        print("host is creating a room...")
        game_rooms[room] = {
            "id": room,
            "host": user,
            "game_started": False,
            "player_map": {userId: "player1"},
            "player_data": {"player1": {"user": user, "userId": userId, "cards": ["", ""], "cash": 5000, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid, "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-oeyilDG6-xNRqwDmSgqaUe0xefnBfVNwNw&usqp=CAU"},
                            "player2": {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": "", "image": "https://images.immediate.co.uk/production/volatile/sites/3/2023/03/Untitled-dfa3422.jpg?quality=90&resize=667,445"},
                            "player3": {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": "", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-oeyilDG6-xNRqwDmSgqaUe0xefnBfVNwNw&usqp=CAU"},
                            "player4": {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": "", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-oeyilDG6-xNRqwDmSgqaUe0xefnBfVNwNw&usqp=CAU"},
                            "player5": {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": "", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-oeyilDG6-xNRqwDmSgqaUe0xefnBfVNwNw&usqp=CAU"},
                            "player6": {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": "", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-oeyilDG6-xNRqwDmSgqaUe0xefnBfVNwNw&usqp=CAU"}},

            "all_player_cards": ["player1", "player2", "player3", "player4", "player5", "player6"],
            "table_cards": [],
            "deck": [],
            "last_card_dealt": 0,
            "player_ids": [userId],
            "player_order": ["player1"],
            "round_order": [],
            "current_turn": 0,
            "turn_number": 0,
            "player_cards_dealt": False,
            "player_cards_dealing": False,
            "flop_dealt": False,
            "turn_dealt": False,
            "river_dealt": False,
            "pot": 0,
            "min_bet": 0,
            "betting_round": "",
            "last_raise": "",
            "players_folded_list": [],
            "players_all_in": [],
            "raise_occurred": False,
            "pregame_bets_taken": False,
            "pregame_bets_completed": False,
            "flop_bets_taken": False,
            "flop_bets_completed": False,
            "turn_bets_taken": False,
            "turn_bets_completed": False,
            "river_bets_taken": False,
            "river_bets_completed": False,
            #INTEGRATION CODE 2/20
            "min_all_in": [],
            "pots": [],
            "bets": [],
            "main_pot": True,
            #----------------------
            "disconnected_players": [],
            "betting_index": 0,
            "winners_declared": False,
            "winners": [],
            "game_over": False
        }
        players_in_games[request.sid] = [room, user, request.sid]
        game = game_rooms[room]

        socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"], "ids": game["player_ids"]}, room = room )
    # print(game_rooms.get(room))
    # print("User was added or rejoined a room")
    print(players_in_games)

@socketio.on('shuffleDeck')
def handle_shuffled_deck(deck_data):
    room = deck_data["room"]
    game = game_rooms.get(room)
    print("\nshuffling deck")
    game["deck"] = deck_data["deck"]
    print(deck_data["deck"][0])
    # socketio.emit('shuffleDeck', deck_data['deck'], room = room) 

@socketio.on('start_game')
def handle_game_start(data):
    room = data["room"]
    game = game_rooms.get(room)
    game["deck"] = data["deck"]
    #added 3/4 ----
    game["game_started"] = True
    print("\nserver letting players know game is starting...and shuffling deck")
    print(data["deck"][0])
    socketio.emit('starting', game, room = room)
#ORIGINAL VERSION OF DEAL CARDS
# @socketio.on('deal_cards')
# def deal_cards(data):
#     print("\ndeal cards is running....")
#     room = data["room"]
    
#     # cards = data["cards"]
#     game = game_rooms.get(room)
#     cards = game["deck"]
#     cards_dealt = game["player_cards_dealt"]
#     if not cards_dealt:
#         #THIS FUNCTION MAY BE ABLE TO RUN BY USING SYSTEM OF DISPLAY CARDS ON FRONTEND 
#         #WOULD NEED TO REMOVE INDIVIDUAL PLAYERCARDS LIST BEING USED WOULD PROBABLY RUN OPTIMALLY AS IT ONLY RUNS ONCE
#         game["betting_round"] = "pregame"
#         game["player_cards_dealing"] = True
#         for player_name in game["player_order"]:
#             players_data = game["player_data"][player_name]
#             # game["current_turn"] = player_name
#             players_data["cards"].append(cards[game["last_card_dealt"]])
#             players_data["cards"].append(cards[game["last_card_dealt"] + 1])
#             game["all_player_cards"].append({player_name: players_data["cards"]})
#             #adding in security so game at player cards dealt is only set to true once last set of cards have been emitted
#             if player_name != game["player_order"][len(game["player_order"]) - 1]:
#                 socketio.emit("dealing", {"user": player_name, "cards": players_data["cards"], "all_player_cards": game["all_player_cards"], "dealing": game["player_cards_dealing"]}, room = room)
#                 print("emitted")
#             else:
#                 game["player_cards_dealt"] = True
#                 socketio.emit("dealing", {"user": player_name, "cards": players_data["cards"], "all_player_cards": game["all_player_cards"], "player_cards_dealt": game["player_cards_dealt"], "dealing": game["player_cards_dealing"]}, room = room)
#                 print("emitted")
#             game["last_card_dealt"] += 2
#             game["last_card_dealt"] += 1
#         print(game["player_data"])

@socketio.on('deal_cards')
def deal_cards(data):
    print("\ndeal cards is running....")
    room = data["room"]
    
    # cards = data["cards"]
    game = game_rooms.get(room)
    cards = game["deck"]
    cards_dealt = game["player_cards_dealt"]
    if not cards_dealt:
        game["betting_round"] = "pregame"
        game["player_cards_dealing"] = True
        game["player_cards_dealt"] = True

        # for player_name in game["player_order"]:
        #     players_data = game["player_data"][player_name]

        #     # game["current_turn"] = player_name
        #     players_data["cards"].append(cards[game["last_card_dealt"]])
        #     players_data["cards"].append(cards[game["last_card_dealt"] + 1])
        #     game["all_player_cards"].append({player_name: players_data["cards"]})

        #     #adding in security so game at player cards dealt is only set to true once last set of cards have been emitted
        #     game["last_card_dealt"] += 2
        #     game["last_card_dealt"] += 1
        # print(game["player_data"])
        # socketio.emit("dealing", {"all_player_cards": game["all_player_cards"],"player_cards_dealt": game["player_cards_dealt"], "dealing": game["player_cards_dealing"]}, room = room)
        # pass
        print(game["player_order"])
        for player in game["player_order"]:
            #player1, player2...
            player_data = game["player_data"][player]
            player_id = player_data["userId"]
            player_cash = player_data["cash"]

            # game["current_turn"] = player_name
            if player_id and player_cash > 0: 
                game["round_order"].append(player)
                player_data["cards"] = []
                player_data["cards"].append(cards[game["last_card_dealt"]])
                player_data["cards"].append(cards[game["last_card_dealt"] + 1])


            # game["all_player_cards"].append({player_name: player_data["cards"]})
                
            
                #Not enough players to properly play 

            #adding in security so game at player cards dealt is only set to true once last set of cards have been emitted
            game["last_card_dealt"] += 2
            game["last_card_dealt"] += 1
        print(game["player_data"])
        socketio.emit("dealing", {"adding_cards": game["player_data"],"player_cards_dealt": game["player_cards_dealt"], "dealing": game["player_cards_dealing"]}, room = room)


@socketio.on("deal_flop")
def deal_flop(data):
    print("\ndealing the flop...")
    
    room = data["room"]
    game = game_rooms.get(room)
    cards = game["deck"]
    if not game["flop_dealt"]:
        print("running flop logic....")
        print(game["table_cards"])
        game["betting_round"] = "flop"
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        game["last_card_dealt"] += 1
        # game["turn_number"] += 1
        print(f'These are the table cards: \n {game["table_cards"]}')
        socketio.emit("dealing_flop", {"table_cards": game["table_cards"], "dealt": True}, room = room)
        game["flop_dealt"] = True

@socketio.on("deal_turn")
def deal_turn(data):
    room = data["room"]
    game = game_rooms.get(room)
    if not game["turn_dealt"]:
        print("\ndealing the turn...")
        cards = game["deck"]
        game["betting_round"] = "turn"
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        game["last_card_dealt"] += 1
        socketio.emit("dealing_turn", {"table_cards": game["table_cards"]}, room = room)
        game["turn_dealt"] = True

@socketio.on("deal_river")
def deal_river(data):
    room = data["room"]
    game = game_rooms.get(room)
    if not game["river_dealt"]:
        print("\ndealing the river...")
        cards = game["deck"]
        game["betting_round"] = "river"
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        socketio.emit("dealing_river", {"table_cards": game["table_cards"]}, room = room)
        game["river_dealt"] = True

@socketio.on("initiate_betting")
def initiate_betting(data):
    #RETURN POINT DELTE IF WORKING WHEN DONE....
    # print("breaks")
    # pass
    room = data["room"]
    game = game_rooms.get(room)
    round = game["betting_round"]
    round_key = str(round) + "_bets_taken"
    print(round_key)
    print("\ninitiating betting is running")
    if not game[round + "_bets_taken"]:
        starting_player = game["current_turn"]
        player = game["round_order"][starting_player]
        #player1 or player2 or ....etc
        player_data = game["player_data"][player]
        player_status = player_data["status"]

        #ADDED 2/17 to account for all players either all in or folded or mix of both
        #4 in player order                      0                                   3
        if (len(game["round_order"]) - len(game["players_folded_list"]) <= 1):
            #ALL BUT ONE PLAYER HAS FOLDED NO MORE BETTING WINNER CAN NOW BE DECLARED
            print(len(game["round_order"]))
            print(len(game["players_folded_list"]))
            print("all but one is folded end betting round end game")
            game["bets"] = []
            game["min_all_in"] = []
            game[round + "_bets_taken"] = True
            game[round + "_bets_completed"] = True

            reset_betting(room, game)

            #SHOULD SET ALL CARDS AS DEALT AND ALL BETS AS TAKEN TO END GAME AND RUN NO MORE LOGIC...
            socketio.emit("end_betting_round", {"game_update": game}, room = room)
        elif (len(game["round_order"]) - (len(game["players_folded_list"]) + len(game["players_all_in"])) == 0):
            #ALL PLAYERS ARE EITHER FOLDED OR ALL IN
            print("all are either folded or all in so end round end game")
            game["bets"] = []
            game["min_all_in"] = []
            game[round + "_bets_taken"] = True
            game[round + "_bets_completed"] = True

            reset_betting(room, game)
            socketio.emit("end_betting_round", {"game_update": game}, room = room)
        elif (len(game["round_order"]) - (len(game["players_all_in"]) + len(game["players_folded_list"])) == 1):
            #THIS SHOULD CAPTURE IF ALL PLAYERS ARE ALL IN AND ONE PLAYER JUST CALLED
            print("all but one have gone all in but that player called or raised previously so end round end game")
            game["bets"] = []
            game["min_all_in"] = []
            game[round + "_bets_taken"] = True
            game[round + "_bets_completed"] = True

            reset_betting(room, game)
            socketio.emit("end_betting_round", {"game_update": game}, room = room)
        else:
            if player_status == "all_in" or player_status == "fold":
                game["current_turn"] +=1
                while game["current_turn"] < len(game["round_order"]):
                    # next_player = game["player_order"][game["current_turn"]]
                    # next_player_data = game["player_data"][next_player]
                    starting_player = game["current_turn"]
                    player = game["round_order"][starting_player]
                    player_data = game["player_data"][player]
                    if player_data["status"] == "fold":
                        game["current_turn"] +=1
                        # starting_player = game["current_turn"]
                        # player = game["player_order"][starting_player]
                        # player_data = game["player_data"][player]
                    elif player_data["status"] == "all_in":
                        game["current_turn"] +=1
                        # starting_player = game["current_turn"]
                        # player = game["player_order"][starting_player]
                        # player_data = game["player_data"][player]
                    else:
                        # starting_player = game["current_turn"]
                        # player = game["player_order"][starting_player]
                        # player_data = game["player_data"][player]
                        break

            if game["current_turn"] == len(game["round_order"]):
                print("Betting has ended we need to comm with front end")
                game[round + "_bets_completed"] = True
                reset_betting(room, game)
                game[round + "_bets_taken"] = True
                socketio.emit("end_betting_round", {"game_update": game}, room = room)
            else:
                min_bet_difference = game["min_bet"] - game["player_data"][player][round]

                
                user_id = game["player_data"][player]["userId"]
                player_bankroll = game["player_data"][player]["cash"]
                game["player_data"][player]["myTurn"] = True

                game[round + "_bets_taken"] = True

                #SOLUTION TO TIMING OUT
                game["time"] = 15
                game["betting_index"] = 0
                current_bet_id = game["betting_index"]

                socketio.emit("take_bet", {"game_update": game, "player_cash": player_bankroll, "user": user_id, "bet_difference": min_bet_difference}, room = room)
                while game["time"] > -1:
                    if game["betting_index"] != current_bet_id:
                        break
                    game["time"] -=1
                    if game["time"] == 0:
                        print("OUT OF TIME EXECUTE FUNCTION!!! CLOSE BETTING!")
                    print(game["time"])
                    time.sleep(1)
                

def auto_fold():
    #THINKING
        #When a player refreses they disconnect and using socket id we can still get game info and swap hosts and put playerid in disconnected players
            #Then delete player from player in game
            #If this player is called to bet the game will auto fold them
                #If player rejoins game the game will again add the id to players in games


        #when a player refreshes if host swap the host and help them reconnect

        #If last player disconnects and nobody left to be host
            #Maybe here can set timer for 5 sec to see if anyone comes back if nobody back using ids
                #if nobody returns emit a game closed to to many disconnected players 
                #alternatively if one returns can (prob not the one to go with ) set all variables to complete with this person as winner and set game start to false....idk bout this one... 


    #IF BETTER IS NOT IN DISCONNECTED PLAYERS
        #SHOULD set display to FALSE
        #SHOULD EMIT BET AS A FOLD
    #IF BETTER IS IN DISCONNECTED PLAYERS
        #SHOULD  
    print("OUT OF TIME!!!!!!!")


@socketio.on("handle_bet_action")
def handle_bet_action(data):
    #2/17 addeding updates to all player cards sections for cash and status
    room = data["room"]
    game = game_rooms.get(room)

    user_id = data["userId"]
    user_name = data["user"]

    player_name = game["player_map"][user_id]

    status = data["bet_status"]
    bet_amount = int(data["bet"])
    player_data = game["player_data"][player_name]
    #This turns off my turn for player ---if presenting problems can also do this right after take bet occurs
    game["player_data"][player_name]["myTurn"] = False
    round = game["betting_round"]

    game["betting_index"] += 1

    print("\nThis is the player that just had an opportunity to bet, their data is being received")
    print(player_name)
    print(f"This player's betting status is {status}.....\n")
    #update the game status with the new data
    #update the players info with new data
    #add total bet to pot
    #increment current_turn

    # game["pot"] += bet_amount

    player_data[round] += bet_amount
    game["player_data"][player_name]["cash"] -= bet_amount


    #Have to add the difference with the previous bet amount
    #if this is a restarted round because of raise my bet minimum will be the difference
    #between last raise and my last bet so if 20 and 10 i must bet at least 10 which is
    #the amount registerd as bet amount but I'm actually betting a total of 20

    #removed 3/1 for bet system to work properly with side pots...
    # bet_amount = player_data[round]

    # if bet_amount > game["min_bet"]:
    #     game["min_bet"] = bet_amount

    if status == "call":
        player_data["status"] = "call"
    if status == "raise":
        game["raise_occurred"] = True
        game["last_raise"] = player_name
        player_data["status"] = "raise"
        # print(f'{game["last_raise"]}, was the last to raise')
    if status == "fold":
        player_data["status"] = "fold"
        game["players_folded_list"].append(player_name)

        #INTEGRATION 2/20/24 ------------------------
        # THIS REMOVES THE LAST MIN ALL IN BET WHEN A PLAYER
        # WITH ENOUGH MONEY FOLDS

        #Analysis on 2/21 shows this might no longer be needed...no longer relying on money amounts...

        # We want to get the max from min_all_in
        print("THIS IS THE PLAYER FOLDING : " + str(player_name))
        print("THIS IS THE PLAYER DATA OF THE PLAYER FOLDING : " + str(player_data))
        print("THIS IS THE PLAYER'S DATA FROM THE GAME : " + str(game["player_data"][player_name]))
        if (len(game["min_all_in"]) > 0):
            if (player_data["cash"] > max(game["min_all_in"])):
                print("THIS IS TRUE")
                print("THIS IS THE CASH: " + str(player_data["cash"]))
                print("THIS IS THE MAX MIN ALL IN BET : " + str(max(game["min_all_in"])))
                if (len(game["min_all_in"]) > 0 and len(game["pots"]) > 0):
                    max_all_in = max(game["min_all_in"])
                    game["min_all_in"].remove(max_all_in)
                    game["pots"].pop()
        #------------------------------------------------
    if status == "all_in":
        player_data["status"] = "all_in"
        game["players_all_in"].append(player_name)
        #Added if conditon here 2/17 to allow cycle back if the all in is the only raise
        if bet_amount > game["min_bet"]:
            game["last_raise"] = player_name
            game["raise_occurred"] = True
            print("There was an all in raise....")
        #INTEGRATION 2/20/24 ---------------------
        if (bet_amount != game["min_bet"]):
            if (bet_amount not in game["min_all_in"]):
                game["min_all_in"].append(bet_amount)
                game["pots"].append({"cash" : 0, "players" : []})
        #-------------------------------------------
    
    #INTEGRATION 2/20/24 --------------------------
    print("min_all_in" + str(game["min_all_in"]))
    print(game["pots"])
    game["bets"].append({"player_name" : player_name, "bet" : bet_amount})
    print("Line 542, These are all the games bets: ")
    print(game["bets"])
    # ----------------------------------------------

    game["current_turn"] += 1

    #MOVED THIS HERE SO GAME CAN RECOGNIZE ALL IN BETS 2/17
    if bet_amount > game["min_bet"]:
        game["min_bet"] = bet_amount
    #CHECK IF NEXT PLAYER IS ALL IN OR HAS FOLDED IF SO SKIP THEM AND INCREMENT AGAIN
   
    while game["current_turn"] < len(game["round_order"]):
        next_player = game["round_order"][game["current_turn"]]
        next_player_data = game["player_data"][next_player]
        if next_player_data["status"] == "fold":
            game["current_turn"] +=1
        elif next_player_data["status"] == "all_in":
            game["current_turn"] +=1
        elif next_player_data["status"] == "raise" and next_player == game["last_raise"]:
            print(f'{next_player} was last to raise game should prepare to stop here')
            print(f'was there a raise? ... {game["raise_occurred"]}')
            game["current_turn"] = len(game["round_order"])
        else:
            break


    if game["current_turn"] == len(game["round_order"]) and game["raise_occurred"]:
        #if all players have betted and a raise occurred reset the current turn number to 0
        #call function that will continue the betting make sure first player has not folded
        
        
        #ADDING CHECK IF ALL PLAYERS FOLDED HERE 2/17
        if (len(game["round_order"]) - len(game["players_folded_list"]) <= 1):
            #ALL BUT ONE PLAYER HAS FOLDED NO MORE BETTING WINNER CAN NOW BE DECLARED
            # game["bets"] = []
            # game["min_all_in"] = []
            # game[round + "_bets_taken"] = True
            # game[round + "_bets_completed"] = True
            print("IS THIS RUNNING FOR SOME REASON???")
            game["current_turn"] = len(game["round_order"])
            game["raise_occurred"] = False

        print("this round should restart at least once...")
        restart_betting_round(room, game)
        while game["current_turn"] < len(game["round_order"]):
            next_player = game["round_order"][game["current_turn"]]
            next_player_data = game["player_data"][next_player]
            if next_player_data["status"] == "fold":
                game["current_turn"] +=1
            elif next_player_data["status"] == "all_in":
                #Added this if condition 2/17 to account for all in raises the regular condition is just current turn + 1
                if next_player == game["last_raise"]:
                    game["current_turn"] = len(game["round_order"])
                else:
                    game["current_turn"] +=1
            elif next_player_data["status"] == "raise" and next_player == game["last_raise"]:
                print(f"{next_player} was last to raise game should stop here")
                print(f'was there a raise? ... {game["raise_occurred"]}')
                game["current_turn"] = len(game["round_order"])
            else:
                break
        # continue_betting(room, game)
    if game["current_turn"] == len(game["round_order"]) and not game["raise_occurred"]:
        #Betting has ended and raise did not occur
        #Call function that will reset the statuses of the players bets
        #put player in front at the end now 
        #may need to make copy of player order to hold original order in game 1 is for betting the other for after the game is over
        #min bet must return to 0 for next betting round
        #set flop complete to true and emit this to front end - maybe do this in function mentioned above
        print("Betting has ended we need to comm with front end")
        game[round + "_bets_taken"] = True
        game[round + "_bets_completed"] = True


        # # --------------- POT LOGIC ---------------

        # If small pots exists
        if (len(game["pots"]) > 0):


            # # We want to subtract the min_all_in from
            # # all the bets that happened this round
            # # excluding any zeroes or numbers that are less
            # min_all_in_bet = min(game["min_all_in"])
            # for i in range(len(game["bets"])):
            #     # Checking if the nth bet is greater or equal to the min_all_in
            #     if (game["bets"][i]["bet"] > min_all_in_bet):
            #         # Getting the difference Example: 750 (player's bet) - 400 (min_all_in) = 350
            #         difference = game["bets"][i]["bet"] - min_all_in_bet
            #         # Subtracting that difference from the nth bet. 750 - 350 = 400
            #         game["bets"][i]["bet"] -= difference
            #         # Add the difference into the last small pot
            #         game["pots"][0]["cash"] += difference
            #         # adding the player that betted in to the players array of that pot to
            #         # let the game know that, that player can play in this pot
            #         game["pots"][0]["players"].append(game["bets"][i]["player_name"])
            # game["min_all_in"].remove(min_all_in_bet)
            


            # --------------- POT LOGIC ---------------
            # THIS SECTION IS IF THERE ARE MORE THAN 1 MIN ALL BET
            
            while (len(game["min_all_in"]) > 0):
                # Getting the min all bet and its respective index
                min_all_bet = min(game["min_all_in"])
                min_all_bet_index = game["min_all_in"].index(min_all_bet)

                for i in range(len(game["bets"])):
                    if (game["bets"][i]["bet"] >= min_all_bet):
                        # Getting the difference Example: 750 (player's bet) - 400 (min_all_in) = 350
                        difference = game["bets"][i]["bet"] - min_all_bet
                        # Subtract that difference from the nth bet. 750 - 350 = 400
                        game["bets"][i]["bet"] -= min_all_bet
                        # Adding that difference to the respective pot
                        if (game["main_pot"]):
                            game["pot"] += min_all_bet
                        else:
                            respective_pot = game["pots"][len(game["pots"]) - len(game["min_all_in"]) - 1]
                            respective_pot["cash"] += min_all_bet
                            # game["bets"][i]["bet"] -= min_all_bet
                            if (game["bets"][i]["player_name"] not in respective_pot["players"]):
                                    respective_pot["players"].append(game["bets"][i]["player_name"])
                game["main_pot"] = False

                for i in range(len(game["min_all_in"])):
                    game["min_all_in"][i] -= min_all_bet
                game["min_all_in"].pop(min_all_bet_index)

            for i in range(len(game["bets"])):
                if (game["bets"][i]["bet"] > 0):
                    game["pots"][len(game["pots"]) - 1]["cash"] += game["bets"][i]["bet"]
                    game["pots"][len(game["pots"]) - 1]["players"].append(game["bets"][i]["player_name"])

            # for i in range(len(game["bets"])):
            #     print("This is the main pot: " + str(game["pot"]))
            #     print("This is how much is getting added: " + str(game["bets"][i]["bet"]))
            #     game["pot"] += game["bets"][i]["bet"]
            #     print("This is the main pot after getting added: " + str(game["pot"]))
        # No small pots exists
        else:
            for i in range(len(game["bets"])):
                    print("This is the main pot: " + str(game["pot"]))
                    print("This is how much is getting added: " + str(game["bets"][i]["bet"]))
                    game["pot"] += game["bets"][i]["bet"]
                    print("This is the main pot after getting added: " + str(game["pot"]))

        # --------------- POT LOGIC ---------------

        print("These are the pots " + str(game["pots"]))
        print("This is min all in" + str(game["min_all_in"]))
        print("These are the bets" + str(game["bets"]))
        print("This is the main pot " + str(game["pot"]))
        game["bets"] = []
        game["min_all_in"] = []


        reset_betting(room, game)
        # socketio.emit("handle_cash", {"game_update": game, "player" : player_name, "player_cash" : player_data["cash"]}, room = room)
        socketio.emit("end_betting_round", {"game_update": game}, room = room)
        #remove this after testing of refreshes 2/9/24
        print("The betting round has ended \n")
    else:
        #still more players to cycle through original betting round
        #call copy of initiate bets to handle next better
        print("handling cash...")
        # socketio.emit("handle_cash", {"game_update": game, "player" : player_name, "player_cash" : player_data["cash"]}, room = room)
        continue_betting(room, game)
        pass

@socketio.on("check_win")
def winner_winner_chicken_dinner(data):
    room = data["room"]
    game = game_rooms.get(room)
    # print("Somebody won!!")
    
    #PRE INTEGRATION 2/20/24
    # game_winners = determine_winner(game)
    # print(game_winners)
    

    if game["winners_declared"] == False:
        game["winners_declared"] = True
        print("declaring winners still runs even with the caviot above...") 
        players_not_playing = []
        print("THESE ARE THE POTS BEFORE REMOVING EMPTY SIDE POTS : " + str(game["pots"]))

        # Removing any empty pots that are still remaining
        for i in range(len(game["pots"])):
            if len(game["pots"][i]["players"]) == 0 and game["pots"][i]["cash"] == 0:
                game["pots"].pop(i)

        print("THESE ARE THE SIDE POTS AFTER REMOVING EMPTY SIDE POTS : " + str(game["pots"]))

        for player in game["players_folded_list"]:
            players_not_playing.append(player)

        if (len(game["pots"]) > 0):
            print("SINCE THERE ARE SMALL POTS WE WILL RUN THOSE SMALL POTS FIRST")
            while (len(game["pots"]) > 0):
                # getting the active pot
                pot_in_play = game["pots"][len(game["pots"]) - 1]
                print("THIS IS THE POT IN PLAY RIGHT NOW : " + str(pot_in_play))
                players_playing = {}

                # Getting all the players that can be in play of the active pot
                #Sergio NEED change to eman game 2/28 ------------- change game at player data to game at round order...
                for player_name in game["round_order"]:
                    if player_name in pot_in_play["players"]:
                        players_playing[player_name] = game["player_data"][player_name]

                print("THESE ARE THE PLAYERS PLAYING IN THE POT IN PLAY : " + str(players_playing))

                # Gets the winning players as a list
                winning_players = determine_winner(game, players_playing)

                print("THESE ARE THE WINNING PLAYERS OF THE POT IN PLAY : " + str(winning_players))

                # Adds the losers to the not in play list
                for i in range(len(pot_in_play["players"])):
                    if (pot_in_play["players"][i] not in winning_players):
                        players_not_playing.append(pot_in_play["players"][i])

                print("THESE ARE THE LOSERS AND NO LONGER IN PLAY : " + str(players_not_playing))

                print("THESE ARE THE POTS BEFORE REMOVING THE LOSERS : " + str(game["pots"]))
                # Removing the the losing players from the other pots
                for i in range(len(game["pots"]) - 1):
                    for player in game["pots"][i]["players"]:
                        if player in players_not_playing:
                            game["pots"][i]["players"].remove(player)

                print("THESE ARE THE POTS AFTER REMOVING THE LOSERS : " + str(game["pots"]))

                print("THESE ARE THE PLAYERS BEFORE CASH EARNINGS WON : " + str(game["player_data"]))

                # Distributing the prize earnings from pot evenly to the winning players
                #Made change here on 3/1 changed player data to round order
                for player in game["round_order"]:
                    if player in winning_players:
                        game["player_data"][player]["cash"] += pot_in_play["cash"] // len(winning_players)

                print("THESE ARE THE PLAYERS AFTER CASH EARNINGS WON : " + str(game["player_data"]))

                # Removes the last pot from the pots because we are done using this pot and no longer need it
                print("THESE ARE THE POTS BEFORE REMOVING : " + str(game["pots"]))
                game["pots"].pop()

                print("THESE ARE THE POTS AFTER REMOVING THE LAST POT : " + str(game["pots"]))
            
            # When the pots while loop are done meaning there are no pots
            # left to play and they are all played, then we will run the main pot
            
            # RUNNING THE MAIN POT HERE
            players_playing = {}

            print("THESE ARE THE PLAYERS NOT PLAYING : " + str(players_not_playing))

            # Adding all players available to play for the main pot
            #CHANGE made here from player_data to round order
            for player_name in game["round_order"]:
                if player_name not in players_not_playing:
                    players_playing[player_name] = game["player_data"][player_name]

            print("THESE ARE THE PLAYERS PLAYING IN THE MAIN POT : " + str(players_playing))

            # Getting back a list of winning players
            winning_players = determine_winner(game, players_playing)

            print("THESE ARE THE WINNERS OF THE MAIN POT : " + str(winning_players))

            print("THIS IS THE AMOUNT THE MAIN POT HAS : " + str(game["pot"]))

            print("THESE ARE THE PLAYERS BEFORE EARNINGS : " + str(game["player_data"]))

            # Distributing the earnings from the Main Pot to the winning players
            #Change here as well 3/1 player data swapped to round order
            for player_name in game["round_order"]:
                if player_name in winning_players:
                    game["player_data"][player_name]["cash"] += game["pot"] // len(winning_players)

            print("THESE ARE THE PLAYERS AFTER EARNINGS : " + str(game["player_data"]))

            game["pot"] = 0
            

            game["winners"] = winning_players
            # game["winners_declared"] = True
            socketio.emit("returning_winners", {"winners": game["winners"], "game_update": game}, room = room)

        # if no small pots exists then we will just run the main pot
        else:
            print("SINCE THERE ARE NO SMALL POTS WE WILL JUST RUN THE MAIN POT")
            players_playing = {}

            # Adding all players available to play for the main pot
            #Sergio change to eman game 2/28 ------------- change game at player data to game at round order...
            for player_name in game["round_order"]:
                if player_name not in players_not_playing:
                    players_playing[player_name] = game["player_data"][player_name]

            print("THESE ARE THE PLAYERS PLAYING : " + str(players_playing))

            # Getting back a list of winning players
            winning_players = determine_winner(game, players_playing)

            print("THESE ARE THE WINNING PLAYERS : " + str(winning_players))

            print("THIS IS THE MAIN POT : " + str(game["pot"]))

            print("THESE ARE THE PLAYERS BEFORE EARNINGS : " + str(game["player_data"]))

            # Distributing the earnings from the Main Pot to the winning players
            #round order instead of player_data
            for player_name in game["round_order"]:
                if player_name in winning_players:
                    game["player_data"][player_name]["cash"] += game["pot"] // len(winning_players)

            print("THESE ARE THE PLAYERS AFTER EARNINGS : " + str(game["player_data"]))

            game["pot"] = 0


        #PRE INTEGRATION GAME WINNNERS LIST
        # game["winners"] = game_winners
            game["winners"] = winning_players
            # game["winners_declared"] = True
            # socketio.emit("returning_winners", {"winners": game["winners"], "winners_declared": game["winners_declared"]}, room = room)
            socketio.emit("returning_winners", {"winners": game["winners"], "game_update": game}, room = room)
   
@socketio.on("restart_the_game")
def restart_the_game(data):
    room = data["room"]
    game = game_rooms.get(room)

    #MAYBE put in a boolean that catches if this has already begun to run like so it can't happen twice

    #Should remove any disconnected players first
    #Insert this logic here ----
    start_next_game(room, game)
    game["deck"] = data["deck"]

    socketio.emit("starting", game, room=room)






#HELPER FUNCTIONS -------------------------------------------------------
def continue_betting(room, game):
    print("\nBetting round has not completed so betting is continuing")
    round = game["betting_round"]
    
    player_index = game["current_turn"]
    player = game["round_order"][player_index]
    player_data = game["player_data"][player]
    user_id = player_data["userId"]

    print("This player will now bet -----")
    print(player)
    min_bet_difference = game["min_bet"] - game["player_data"][player][round]
    #added bankroll to put a cap on max bet someone can put in
    player_bankroll = player_data["cash"]

    current_bet_id = game["betting_index"]

    #ADDED 2/17 to end game if all other players have folded...the else was the regular piece of code before this if 
    if (len(game["round_order"]) - len(game["players_folded_list"]) <= 1):
        #ALL BUT ONE PLAYER HAS FOLDED NO MORE BETTING WINNER CAN NOW BE DECLARED
        game["bets"] = []
        game["min_all_in"] = []
        game[round + "_bets_taken"] = True
        game[round + "_bets_completed"] = True

        reset_betting(room, game)
        socketio.emit("end_betting_round", {"game_update": game}, room = room)
    else:
        game["player_data"][player]["myTurn"] = True
        socketio.emit("take_bet", {"game_update": game, "player_cash": player_bankroll, "user": user_id, "bet_difference": min_bet_difference}, room = room)

    #LOGIC FOR HANDLING TIME OUTS ON BETTING ---------------------------------------------------------------------
    # time.sleep(15)
    # print("desycronized check that occurs when 10 seconds pass from take bet function might be a problem, maybe not?")
    # # print("player has folded...too much time passed")
    # if game["betting_index"] == current_bet_id:
    #     print("time maxed out and a bet was not received, will emit fold this is is continue betting")
    #     player_data["status"] == "fold"
    #     socketio.emit("fold_for_player",{"folded_player": player, "updated_player_data": game["player_data"]}, room = room)
    # else: 
    #     print("bet was received :) in continue betting\n")
    # #If the last bet sent out was not received fold for this player and 
    # #maybe can emit something to new host to receive and pass along to game as sub in for  
    # #how can I check that the last bet was sent out to Sergio and he never 

def reset_betting(room, game):
    round = game["betting_round"]
    print("\nreseting the betting round")
    # Reseting most of everything in game object after betting round is over
    # for whatever round that is

    # Give pot money to the winners.
    game["last_raise"] = ""
    game["raise_occurred"] = False
    # game["betting_round"] = ""
    game["min_bet"] = 0

    #WHY WOULD THE FOLDED PLAYERS RESET? ASK EMAN 2/17
    # game["players_folded_list"].clear()

    for player in game["player_data"]:
        status = game["player_data"][player]["status"]
        print(f"{player}'s status is {status} and this decides if its reset")
        if status != "fold" and status != "all_in":
            print(f"reseting {player}'s status")
            game["player_data"][player]["status"] = ""
    # Moving first player to the back
    first_player = game["round_order"].pop(0)
    game["round_order"].append(first_player)
    game["current_turn"] = 0

def restart_betting_round(room, game):
    game["current_turn"] = 0
    game["raise_occurred"] = False

def start_next_game(room, game):

    for player in game["player_data"]:
        player_data = game["player_data"]
        player_data[player]["cards"] = ["", ""]
        player_data[player]["status"] = ""
        player_data[player]["pregame"] = 0
        player_data[player]["flop"] = 0
        player_data[player]["turn"] = 0
        player_data[player]["river"] = 0

    # game["all_player_cards"] = []
    game["table_cards"] = []
    game["deck"] = []
    game["last_card_dealt"] = 0
    #NEED TO SET UP PLAYER ORDER that matches original player order at start of round
    #Remove starting player and add to end
    #Maybe even use 3...1 to keep the very original seats at table?
    game["current_turn"] = 0
    game["turn_number"] = 0
    game["player_cards_dealt"] = False
    game["player_cards_dealing"] = False
    game["flop_dealt"] = False
    game["turn_dealt"] = False
    game["river_dealt"] = False
    game["pot"] = 0
    game["min_bet"] = 0
    game["betting_round"] = ""
    game["last_raise"] = ""
    game["players_folded_list"] = []
    game["players_all_in"] = []
    game["raise_occurred"] = False
    game["pregame_bets_taken"] = False
    game["pregame_bets_completed"] = False
    game["flop_bets_taken"] = False
    game["flop_bets_completed"] = False
    game["turn_bets_taken"] = False
    game["turn_bets_completed"] = False
    game["river_bets_taken"] = False
    game["river_bets_completed"] = False
    game["bet_difference"] = False
    game["disconnected_players"] = []
    game["betting_index"] = 0
    game["winners_declared"] = False
    game["winners"] = []
    game["game_over"] = False
    #Continue adding

    #Need to extract players no longer present meaning any in disconnected players list
    #Extract from player order potentially will have bugs but works...
    #Extract id from player map
    #Reset player data of specific player template to default state without player
    #Extract player id from player ids

    #move front player in order to the back
    print("this was our player order")
    print(game["player_order"])
    game["round_order"] = []
    first_player = game["player_order"].pop(0)
    game["player_order"].append(first_player)
    print(game["player_order"])


def get_high_card(cards):
        values = sorted(card["value"] for card in cards)
        return values[-1]
def is_one_pair(cards):
        values = [card["value"] for card in cards]
        # return any(values.count(value) == 2 for value in set(values))
        pairs = [value for value in set(values) if values.count(value) == 2]
        if len(pairs) > 0:
            return max(pairs)
        else: 
            return False  
def is_two_pair(cards):
        values = [card["value"] for card in cards]
        pairs = [value for value in set(values) if values.count(value) == 2]
        
        #Need to remove Ace that equals 1 and let the function continue to cycle until it find the Ace that's value is 14
        if len(pairs) > 1 and 1 not in values:
            # print(values)
            return max(pairs)
        # return sum(1 for value in set(values) if values.count(value) == 2) == 2
        else:
            return False
def is_three_of_a_kind(cards):
        values = [card["value"] for card in cards]
        # return any(values.count(value) == 3 for value in set(values))
        triples = [value for value in set(values) if values.count(value) == 3]
        if len(triples) > 0:
            return max(triples)
        else:
             return False
def is_straight(cards):
        values = sorted(card["value"] for card in cards)
        # return any(values[i] + 1 == values[i + 1] for i in range(len(values) - 1))
        straight = [values[i] for i in range(len(values) - 1) if values[i] + 1 == values[i + 1] ]
        if len(straight) == 4:
             return max(straight)
        else:
             return False
def is_flush(cards):
        values = []
        suits = []

        for card in cards:
             suit = card["suit"]
             value = card["value"]
             #Accounting for the fact that we added in a possible Ace with 14 value to our combo of cards
             if value == 1:
                  pass
             else:
                suits.append(suit)
                values.append(value)
        # flush = [suit for suit in suits if suits.count(suit) == 5]
        if suits.count(suit) == 5:
            print(cards)
            return max(values)
        else:
            return False
             
        # return any(suits.count(suit) == 5 for suit in set(suits))
def is_full_house(cards):
    values = [card["value"] for card in cards]
    if 1 and 14 in values:
        #This is a case of both Aces being present should be ignored
        return False
    pairs = list(set(values))
    if len(pairs) == 2:
        full_house = [value for value in pairs if values.count(value) == 3]
        if len(full_house) > 0:
            return max(full_house)
    else:
        return False
    
def is_four_of_a_kind(cards):
    values = [card["value"] for card in cards]
    quads = [value for value in set(values) if values.count(value) == 4]
    if len(quads) > 0:
        return max(quads)
    else:
        return False
def is_straight_flush(cards):
    straight = is_straight(cards)
    if straight:
        straight_flush = is_flush(cards)
        if straight_flush:
            return straight_flush
        else:
            return False
    else:
        return False

hand_evaluations = [
    is_straight_flush,
    is_four_of_a_kind,
    is_full_house,
    is_flush,
    is_straight,
    is_three_of_a_kind,
    is_two_pair,
    is_one_pair,
    get_high_card,
    ]

hand_scores = {
    "get_high_card":10,
    "is_one_pair": 20,
    "is_two_pair": 30,
    "is_three_of_a_kind": 40,
    "is_straight": 50,
    "is_flush": 60,
    "is_full_house": 70,
    "is_four_of_a_kind": 80,
    "is_straight_flush": 90,
}

def determine_winner(game, incoming_player_list):
    player_hands = {}
    winners = {}
    winners_check_2 = {}
    winners_check_final = {}

    table_cards = game["table_cards"]

    # for player_info in game["player_list"]:
    #     player = list(player_info.keys())[0]
    #     player_cards = player_info[player]
    #     player_hand = evaluate_hand(player_cards, table_cards, player)
    #     player_hands[player] = player_hand

    #NEW VERSION WITH PLAYER_DATA
    for player_name in incoming_player_list:
        players_data = incoming_player_list[player_name]
        player_cards = players_data["cards"]
        player_hand = evaluate_hand(player_cards, table_cards, player_name)
        player_hands[player_name] = player_hand
    #CAN USE ANYTHING THAT ALREADY CONTAINS NAMES

    player_list = list(player_hands.keys())
    best_score = player_hands[list(player_hands.keys())[0]]["score"]

    for player_name in player_list:
        current_player_hand = player_hands[player_name]
        score = current_player_hand["score"]
        if score > best_score:
            best_score = score
            winners.clear()
            winners[player_name] = current_player_hand
        elif score == best_score:
             winners[player_name] = current_player_hand
    if len(list(winners.keys())) > 1:
        #Second Filter
        print("players had same type of hand so will check further")
        winner_list = list(winners.keys())
        best_score = 0  
        for player_name in winner_list:
            current_player_hand = winners[player_name]
            score = current_player_hand["pair_value"]
            print("This is the score determined by highest pair value: " + str(score))
            if score > best_score:
                best_score = score
                winners_check_2.clear()
                winners_check_2[player_name] = current_player_hand
            elif score == best_score:
                winners_check_2[player_name] = current_player_hand
        if len(list(winners_check_2.keys())) > 1:
            #Final Run Through
            print("Went all the way to final rundown where hand sums are checked")
            winner_list = list(winners_check_2.keys())
            best_score = 0  
            for player_name in winner_list:
                current_player_hand = winners[player_name]
                score = current_player_hand["hand_sum"]
                print("This is the score determined by highest pair value: " + str(score))
                if score > best_score:
                    best_score = score
                    winners_check_final.clear()
                    winners_check_final[player_name] = current_player_hand
                elif score == best_score:
                    winners_check_final[player_name] = current_player_hand
            print("final filter")
            return list(winners_check_final.keys())
        else:
            print("second filter")
            return list(winners_check_2.keys())
    else:
        print("first filter")
        return list(winners.keys())



def evaluate_hand(player_cards, all_table_cards, player):
    print(f"evaluating {player}'s hand...")
    best_hand = {}
    all_cards = player_cards + all_table_cards
    [all_cards.append({"name": "A", "suit": card["suit"], "value": 14}) for card in all_cards if card["value"] == 1]
    all_combinations = list(combinations(all_cards, 5))
    player_card_values = [player_cards[0]["value"], player_cards[1]["value"]]

    max_score = 0
    evalutation_index = 0
    
    for evaluation in hand_evaluations:
        score = 0
        for combination in all_combinations:
            evaluation_result = evaluation(combination)
            if evaluation_result:
                score = hand_scores[evaluation.__name__]
                if score > max_score:
                    max_score = score
                    best_hand = {"name": player, "score": score, 
                                    "pair_value": evaluation_result, "hand_sum": sum(player_card_values)}
                    #adding this in to help stop full cycle through of hand evaluations added 1-3-2024, remove if needed
                    helper_score = score
                elif score == max_score:
                    # if len(best_hand.keys()) > 0:
                    #     print("we attempted")
                    if evaluation_result > best_hand["pair_value"]:
                        
                        best_hand = {"name": player, "score": score, 
                            "pair_value": evaluation_result, "hand_sum": sum(player_card_values)}
    
        evalutation_index +=1
        #If scored exists at a higher hand evaluation such as a straight flush do not proceed with other evalutions
        if max_score > 0 and evalutation_index > 0:
            print(f"Went through {evalutation_index} hand evalutations for {player}. \n")
            # print(best_hand)
            # print("")
            return best_hand     
    return best_hand






if __name__ == '__main__':
    socketio.run(app, debug=True, port=5555)

