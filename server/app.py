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

# Local imports
from config import app, db, api
# Add your model imports
from models import Card



# Instantiate Socket Io
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")


game_rooms = {}
players_in_games = {}
turns_and_card_positions = [{"12": [1, 0]}]

# Views go here!
#RETURN POINT 1/31/2024
    #HERE
@app.route('/')
def index():
    return '<h1>Poker Server</h1>'

class StoreRoomData(Resource):
    def post(self):
        user = request.json["user"]
        code = request.json["room"]
        session["user"] = user
        session["room"] = code

        print("stored data")
        return {"user": user, "room": code }, 200
    
api.add_resource(StoreRoomData, "/storeData")

class CheckSession(Resource):
    def get(self):
        user = session["user"]
        code = session["room"]
        if user and code:
            return {"user": user, "room": code}, 200
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
        return make_response({"room_code": code}, 200)
    
api.add_resource(Room_codes, "/room_codes")

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
    #     if game["host"] == user:



@socketio.on('left_room')
def handle_leaving_room(room_data):
    print(room_data["user"] + " has left the room")

@socketio.on('join_room')
def handle_join_room(room_data):
    print("\nrunning join room")
    room = room_data['room']
    user = room_data['user']
    join_room(room)
    if game_rooms.get(room) is not None:
        if user not in game_rooms.get(room)["player_order"]:
            print("new player has joined the room")
            game_rooms[room]["player_list"].append({user: []})
            #new version of player list below when properly integrated remove old player_list
            game_rooms[room]["player_data"][user] = {"cards" : [], "cash" : 1000, "status" : "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
            game_rooms[room]["player_order"].append(user)

            players_in_games[request.sid] = [room, user]
        else:
            print(f"{user} is rejoining...")
            game = game_rooms[room]
            
            round = game["betting_round"]
            print(f"The round is {round}")
            print(game[round + "_bets_taken"])
            player_cards = game["player_data"][user]["cards"]
            player_money = game["player_data"][user]["cash"]

            min_bet_difference = game["min_bet"] - game["player_data"][user][round]
            #ALLOW PLAYER TO REJOIN TO THEIR PROPER STAGE WITHIN THE GAME
            #MAY WANT TO SET GAME TO FALSE AT START ON BACKEND THEN WITH STARTING SET TO TRUE
            if game["game_started"] and game["player_cards_dealt"] == False:
                print("player will be returned to game with their data recovered")
                socketio.emit('rejoin_game', {"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            elif game["pregame_bets_taken"] == True and game["pregame_bets_completed"] == False:
                if game["player_order"][game["current_turn"]] == user:
                    print(f"letting {user} bet again")
                    print(game["all_player_cards"])
                    socketio.emit('rejoin_at_bet',{"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room)
                else:
                    print("player will be returned to game with their data recovered")
                    socketio.emit('rejoin_game', {"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            elif game["game_started"] and game["flop_dealt"] == False:
                print("player will be returned to game with their data recovered")
                socketio.emit('rejoin_game', {"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            elif game["pregame_bets_completed"] and game["flop_bets_taken"] and game["flop_bets_completed"] == False:
                if game["player_order"][game["current_turn"]] == user:
                    print(f"letting {user} bet again")
                    print(game["all_player_cards"])
                    socketio.emit('rejoin_at_bet',{"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room)
                else:
                    print("player will be returned to the flop betting with their data recovered, but it is not yet their turn")
                    socketio.emit('rejoin_game', {"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            elif game["game_started"] and game["turn_dealt"] == False:
                print("player will be returned to game with their data recovered")
                socketio.emit('rejoin_game', {"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            elif game["flop_bets_completed"] and game["turn_bets_taken"] and game["turn_bets_completed"] == False:
                if game["player_order"][game["current_turn"]] == user:
                    print(f"letting {user} bet again")
                    print(game["all_player_cards"])
                    socketio.emit('rejoin_at_bet',{"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room)
                else:
                    print("player will be returned to the flop betting with their data recovered, but it is not yet their turn")
                    socketio.emit('rejoin_game', {"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            elif game["game_started"] and game["river_dealt"] == False:
                print("player will be returned to game with their data recovered")
                print("river cards should be dealt out directly after?")
                socketio.emit('rejoin_game', {"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            elif game["turn_bets_completed"] and game["river_bets_taken"] and game["river_bets_completed"] == False:
                if game["player_order"][game["current_turn"]] == user:
                    print(f"letting {user} bet again")
                    print(game["all_player_cards"])
                    socketio.emit('rejoin_at_bet',{"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room)
                else:
                    print("player will be returned to the flop betting with their data recovered, but it is not yet their turn")
                    socketio.emit('rejoin_game', {"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
            else:
                #TRYING TO IMPLEMENT THIS AS RETURNING AT ANY OTHER POINT
                print("player will be returned to the flop betting with their data recovered, but just standard in between actions..")
                socketio.emit('rejoin_game', {"game": game, "user": user, "player_cards": player_cards, "player_cash": player_money, "bet_difference": min_bet_difference }, room = room )
    else:
        print("host is creating a room...")
        game_rooms[room] = {
            "id": room,
            "host": user,
            "game_started": True,
            "player_list": [{user: []}],
            "player_data": {user: {"cards": [], "cash": 1000, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}},
            "all_player_cards": [],
            "table_cards": [],
            "deck": [],
            "last_card_dealt": 0,
            "player_order": [user],
            "current_turn": 0,
            "turn_number": 0,
            "player_cards_dealt": False,
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
            "disconnected_players": [],
            "betting_index": 0,
        }
        players_in_games[request.sid] = [room, user]

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

    print("\nserver letting players know game is starting...and shuffling deck")
    print(data["deck"][0])
    socketio.emit('starting', game, room = room)

@socketio.on('deal_cards')
def deal_cards(data):
    print("\ndeal cards is running....")
    room = data["room"]
    turn = int(data["turn"])
    # cards = data["cards"]
    game = game_rooms.get(room)
    cards = game["deck"]
    cards_dealt = game["player_cards_dealt"]
    if not cards_dealt:
        game["betting_round"] = "pregame"
        for player_name in game["player_order"]:
            players_data = game["player_data"][player_name]
            # game["current_turn"] = player_name
            players_data["cards"].append(cards[game["last_card_dealt"]])
            players_data["cards"].append(cards[game["last_card_dealt"] + 1])
            game["all_player_cards"].append({player_name: players_data["cards"]})
            #adding in security so game at player cards dealt is only set to true once last set of cards have been emitted
            if player_name != game["player_order"][len(game["player_order"]) - 1]:
                socketio.emit("dealing", {"user": player_name, "cards": players_data["cards"], "all_player_cards": game["all_player_cards"]}, room = room)
            else:
                game["player_cards_dealt"] = True
                socketio.emit("dealing", {"user": player_name, "cards": players_data["cards"], "all_player_cards": game["all_player_cards"], "player_cards_dealt": game["player_cards_dealt"]}, room = room)
            game["last_card_dealt"] += 2
            game["last_card_dealt"] += 1
        # game["turn_number"] +=1
            
        # game["player_cards_dealt"] = True
        print(game["player_data"])

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
        socketio.emit("dealing_flop", {"table_cards": game["table_cards"]}, room = room)
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
    room = data["room"]
    game = game_rooms.get(room)
    round = game["betting_round"]
    round_key = str(round) + "_bets_taken"
    print(round_key)
    print("\ninitiating betting is running")
    if not game[round + "_bets_taken"]:
        starting_player = game["current_turn"]
        player = game["player_order"][starting_player]
        player_data = game["player_data"][player]
        player_status = player_data["status"]

        if player_status == "all_in" or player_status == "fold":
            game["current_turn"] +=1
            while game["current_turn"] < len(game["player_order"]):
                # next_player = game["player_order"][game["current_turn"]]
                # next_player_data = game["player_data"][next_player]
                starting_player = game["current_turn"]
                player = game["player_order"][starting_player]
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

        if game["current_turn"] == len(game["player_order"]):
            print("Betting has ended we need to comm with front end")
            game[round + "_bets_completed"] = True
            reset_betting(room, game)
            game[round + "_bets_taken"] = True
            socketio.emit("end_betting_round", {"game_update": game}, room = room)
        else:
            min_bet_difference = game["min_bet"] - game["player_data"][player][round]

            current_bet_id = game["betting_index"]

            game[round + "_bets_taken"] = True
            socketio.emit("take_bet", {"game_update": game, "user": player, "bet_difference": min_bet_difference}, room = room)

            # #LOGIC FOR HANDLING TIME OUTS ON BETTING ---------------------------------------------------------------------
            # time.sleep(15)
            # print("desycronized check that occurs when 10 seconds pass from take bet function might be a problem, maybe not?")
            # # print("player has folded...too much time passed")
            # if game["betting_index"] == current_bet_id:
            #     print("time maxed out and a bet was not received")
            #     player_data["status"] == "fold"
            #     socketio.emit("fold_for_player",{"folded_player": player, "updated_player_data": game["player_data"]}, room = room)
            # else: 
            #     print("bet was received :)\n")
            # #If the last bet sent out was not received fold for this player and 
            # #maybe can emit something to new host to receive and pass along to game as sub in for  
            # #how can I check that the last bet was sent out to Sergio and he never 
    
@socketio.on("handle_bet_action")
def handle_bet_action(data):
    room = data["room"]
    game = game_rooms.get(room)

    player_name = data["user"]
    status = data["bet_status"]
    bet_amount = int(data["bet"])
    player_data = game["player_data"][player_name]
    round = game["betting_round"]

    game["betting_index"] += 1

    print("\nThis is the player that just had an opportunity to bet, their data is being received")
    print(player_name)
    print(f"This player's betting status is {status}.....\n")
    #update the game status with the new data
    #update the players info with new data
    #add total bet to pot
    #increment current_turn
    game["pot"] += bet_amount
    player_data[round] += bet_amount
    game["player_data"][player_name]["cash"] -= bet_amount
    #Have to add the difference with the previous bet amount
    #if this is a restarted round because of raise my bet minimum will be the difference
    #between last raise and my last bet so if 20 and 10 i must bet at least 10 which is
    #the amount registerd as bet amount but I'm actually betting a total of 20
    bet_amount = player_data[round]

    if bet_amount > game["min_bet"]:
        game["min_bet"] = bet_amount

    if status == "raise":
        game["raise_occurred"] = True
        game["last_raise"] = player_name
        player_data["status"] = "raise"
        print(f'{game["last_raise"]}, was the last to raise')
    if status == "fold":
        player_data["status"] = "fold"
        game["players_folded_list"].append(player_name)
    if status == "all_in":
        player_data["status"] = "all_in"
        game["players_all_in"].append(player_name)
    game["current_turn"] += 1

    #CHECK IF NEXT PLAYER IS ALL IN OR HAS FOLDED IF SO SKIP THEM AND INCREMENT AGAIN
   
    while game["current_turn"] < len(game["player_order"]):
        next_player = game["player_order"][game["current_turn"]]
        next_player_data = game["player_data"][next_player]
        if next_player_data["status"] == "fold":
            game["current_turn"] +=1
        elif next_player_data["status"] == "all_in":
            game["current_turn"] +=1
        elif next_player_data["status"] == "raise" and next_player == game["last_raise"]:
            print(f'{next_player} was last to raise game should stop here')
            print(f'was there a raise? ... {game["raise_occurred"]}')
            game["current_turn"] = len(game["player_order"])
            socketio.emit("handle_cash", {"game_update": game, "player" : player_name, "player_cash" : player_data["cash"]}, room = room)
            socketio.emit("end_betting_round", {"game_update": game}, room = room)
        else:
            break


    if game["current_turn"] == len(game["player_order"]) and game["raise_occurred"]:
        #if all players have betted and a raise occurred reset the current turn number to 0
        #call function that will continue the betting make sure first player has not folded
        restart_betting_round(room, game)
        while game["current_turn"] < len(game["player_order"]):
            next_player = game["player_order"][game["current_turn"]]
            next_player_data = game["player_data"][next_player]
            if next_player_data["status"] == "fold":
                game["current_turn"] +=1
            elif next_player_data["status"] == "all_in":
                game["current_turn"] +=1
            elif next_player_data["status"] == "raise" and next_player == game["last_raise"]:
                print(f"{next_player} was last to raise game should stop here")
                print(f'was there a raise? ... {game["raise_occurred"]}')
                game["current_turn"] = len(game["player_order"])
                game[round + "_bets_taken"] = True
                game[round + "_bets_completed"] = True
                socketio.emit("handle_cash", {"game_update": game, "player" : player_name, "player_cash" : player_data["cash"]}, room = room)
                socketio.emit("end_betting_round", {"game_update": game}, room = room)
            else:
                break
        # continue_betting(room, game)
    if game["current_turn"] == len(game["player_order"]) and not game["raise_occurred"]:
        #Betting has ended and raise did not occur
        #Call function that will reset the statuses of the players bets
        #put player in front at the end now 
        #may need to make copy of player order to hold original order in game 1 is for betting the other for after the game is over
        #min bet must return to 0 for next betting round
        #set flop complete to true and emit this to front end - maybe do this in function mentioned above
        print("Betting has ended we need to comm with front end")
        game[round + "_bets_taken"] = True
        game[round + "_bets_completed"] = True
        reset_betting(room, game)
        socketio.emit("handle_cash", {"game_update": game, "player" : player_name, "player_cash" : player_data["cash"]}, room = room)
        socketio.emit("end_betting_round", {"game_update": game}, room = room)
        #remove this after testing of refreshes 2/9/24
        print("The betting round has ended \n")
    else:
        #still more players to cycle through original betting round
        #call copy of initiate bets to handle next better
        socketio.emit("handle_cash", {"game_update": game, "player" : player_name, "player_cash" : player_data["cash"]}, room = room)
        continue_betting(room, game)
        pass

@socketio.on("check_win")
def winner_winner_chicken_dinner(data):
    room = data["room"]
    game = game_rooms.get(room)
    # print("Somebody won!!")
    game_winners = determine_winner(game)
    print(game_winners)
    print(game["player_data"])
    socketio.emit("returning_winners", {"winners": game_winners}, room = room)
   



#HELPER FUNCTIONS -------------------------------------------------------
def continue_betting(room, game):
    print("\nBetting round has not completed so betting is continuing")
    round = game["betting_round"]
    
    player_index = game["current_turn"]
    player = game["player_order"][player_index]
    player_data = game["player_data"][player]

    print("This player will now bet -----")
    print(player)
    min_bet_difference = game["min_bet"] - game["player_data"][player][round]

    current_bet_id = game["betting_index"]
    socketio.emit("take_bet", {"game_update": game,"user": player, "bet_difference": min_bet_difference}, room = room)


    # #LOGIC FOR HANDLING TIME OUTS ON BETTING ---------------------------------------------------------------------
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
    game["players_folded_list"].clear()
    for player in game["player_data"]:
        status = game["player_data"][player]["status"]
        print(f"{player}'s status is {status} and this decides if its reset")
        if status != "fold" and status != "all_in":
            print(f"reseting {player}'s status")
            game["player_data"][player]["status"] = ""
    # Moving first player to the back
    first_player = game["player_order"].pop(0)
    game["player_order"].append(first_player)
    game["current_turn"] = 0

def restart_betting_round(room, game):
    game["current_turn"] = 0
    game["raise_occurred"] = False

def start_next_game(room, game):
    game["all_player_cards"] = []
    game["table_cards"] = []
    game["deck"] = []
    game["last_card_dealt"] = 0
    #NEED TO SET UP PLAYER ORDER that matches original player order at start of round
    #Remove starting player and add to end
    #Maybe even use 3...1 to keep the very original seats at table?
    game["current_turn"] = ""
    game["turn_number"] = 0
    game["player_cards_dealt"] = False
    game["flop_dealt"] = False
    game["turn_dealt"] = False
    game["river_dealt"] = False
    game["pot"] = 0
    game["min_bet"] = 0
    game["betting_round"] = ""
    game["last_raise"] = ""
    #Continue adding
    pass

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

def determine_winner(game):
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
    for player_name in game["player_data"]:
        players_data = game["player_data"][player_name]
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
        winner_list = list(winners.keys())
        best_score = 0  
        for player_name in winner_list:
            current_player_hand = winners[player_name]
            score = current_player_hand["pair_value"]
            if score > best_score:
                best_score = score
                winners_check_2.clear()
                winners_check_2[player_name] = current_player_hand
            elif score == best_score:
                winners_check_2[player_name] = current_player_hand
        if len(list(winners_check_2.keys())) > 1:
            #Final Run Through
            winner_list = list(winners_check_2.keys())
            best_score = 0  
            for player_name in winner_list:
                current_player_hand = winners[player_name]
                score = current_player_hand["hand_sum"]
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

