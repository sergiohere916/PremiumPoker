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

# Local imports
from config import app, db, api
# Add your model imports
from models import Card



# Instantiate Socket Io
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")


game_rooms = {}
turns_and_card_positions = [{"12": [1, 0]}]

# Views go here!
#RETURN POINT 1/31/2024
    #HERE
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
            #new version of player list below when properly integrated remove old player_list
            game_rooms[room]["player_data"][user] = {"cards" : [], "cash" : 1000, "status" : 0, "flop": 0, "turn_bet": 0, "river_bet": 0}
            game_rooms[room]["player_order"].append(user)
        else:
            pass
            #RUN SOME FUNCTION OR EMIT ALL GAME DATA ALREADY AVAILABLE FOR USER
    else:
        game_rooms[room] = {
            "id": room,
            "game_started": True,
            "player_list": [{user: []}],
            "player_data": {user: {"cards": [], "cash": 1000, "status": "", "flop": 0, "turn_bet": 0, "river_bet": 0}},
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
            "raise_occurred": False,
            "flop_bets_taken": False,
            "flop_bets_completed": False
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
    # socketio.emit('shuffleDeck', deck_data['deck'], room = room) 

@socketio.on('start_game')
def handle_game_start(data):
    room = data["room"]
    game = game_rooms.get(room)
    game["deck"] = data["deck"]

    print("server letting players know game is starting...and shuffling deck")
    print(data["deck"][0])
    socketio.emit('starting', game, room = room)

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
        # for player_dict in game["player_list"]:
        #     for player in player_dict:
        #         game["current_turn"] = player
        #         player_dict[player].append(cards[game["last_card_dealt"]])
        #         player_dict[player].append(cards[game["last_card_dealt"] + 1])
        #         socketio.emit("dealing", {"user": player, "cards": player_dict[player]}, room = room)
        #     game["last_card_dealt"] += 2
        # game["last_card_dealt"] += 1
        # # game["turn_number"] +=1
        # game["player_cards_dealt"] = True
        # print(game["player_list"])

        for player_name in game["player_data"]:
            players_data = game["player_data"][player_name]
            # game["current_turn"] = player_name
            players_data["cards"].append(cards[game["last_card_dealt"]])
            players_data["cards"].append(cards[game["last_card_dealt"] + 1])
            socketio.emit("dealing", {"user": player_name, "cards": players_data["cards"]}, room = room)
            game["last_card_dealt"] += 2
            game["last_card_dealt"] += 1
        # game["turn_number"] +=1
            
        game["player_cards_dealt"] = True
        print(game["player_data"])

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
        print(game["table_cards"])
        socketio.emit("dealing_flop", {"table_cards": game["table_cards"]}, room = room)
        game["flop_dealt"] = True

@socketio.on("deal_turn")
def deal_turn(data):
    room = data["room"]
    game = game_rooms.get(room)
    if not game["turn_dealt"]:
        print("dealing the turn...")
        cards = game["deck"]
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
        print("dealing the river...")
        cards = game["deck"]
        game["table_cards"].append(cards[game["last_card_dealt"]])
        game["last_card_dealt"] += 1
        socketio.emit("dealing_river", {"table_cards": game["table_cards"]}, room = room)
        game["river_dealt"] = True

@socketio.on("initiate_betting")
def initiate_betting(data):
    room = data["room"]
    game = game_rooms.get(room)
    round = game["betting_round"]
    if not game[f"{round}_bets_taken"]:
        starting_player = game["current_turn"]
        player = game["player_order"][starting_player]
        min_bet_difference = game["min_bet"] - game["player_data"][player][round]
        socketio.emit("take_bet", {"game_update": game, "user": player, "bet_difference": min_bet_difference}, room = room)
        game["flop_bets_taken"] = True
    
@socketio.on("handle_bet_action")
def handle_bet_action(data):
    room = data["room"]
    game = game_rooms.get(room)

    player_name = data["user"]
    status = data["bet_status"]
    bet_amount = int(data["bet"])
    player_data = game["player_data"][player_name]
    round = game["betting_round"]

    print("THIS IS THE PLAYER BETTTINGGG")
    print(player_name)
    print(f"We haveee success, but app breaks here status is {status}.....")
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
    if status == "fold":
        player_data["status"] = "fold"
    if status == "all_in":
        player_data["status"] = "all_in"
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
            print(f"{player_name} was last to raise game should stop here")
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
                print(f"{player_name} was last to raise game should stop here")
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
    socketio.emit("returning_winners", {"winners": game_winners}, room = room)
   



#HELPER FUNCTIONS -------------------------------------------------------
def continue_betting(room, game):
    print("OMGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG THIS IS CONTINUED")
    round = game["betting_round"]
    
    player_index = game["current_turn"]
    player = game["player_order"][player_index]
    print("THIS IS THE PLAYERRRRRRRRR")
    print(player)
    min_bet_difference = game["min_bet"] - game["player_data"][player][round]
    socketio.emit("take_bet", {"game_update": game,"user": player, "bet_difference": min_bet_difference}, room = room)

def reset_betting(room, game):
    round = game["betting_round"]
    
    # Reseting most of everything in game object after betting round is over
    # for whatever round that is

    # Give pot money to the winners.
    game["last_raise"] = ""
    game["raise_occurred"] = False
    game["betting_round"] = ""
    game["min_bet"] = 0
    game["players_folded_list"].clear()
    for player in game["player_data"]:
        game["player_data"][player]["status"] = ""
    # Moving first player to the back
    first_player = game["player_order"].pop(0)
    game["player_order"].append(first_player)
    game["current_turn"] = 0

def restart_betting_round(room, game):
    game["current_turn"] = 0
    game["raise_occurred"] = False


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

