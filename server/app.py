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
from models import User, Card, Tag, Icon, UserIcon, UserTag

# Local imports
from config import app, db, api
# Add your model imports


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

# User Routes
class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(users, 200)
    
    def post(self):
        new_user = User(
            username = request.json["username"]
        )

        db.session.add(new_user)
        db.session.commit()

        return make_response(new_user.to_dict(), 200)
    
api.add_resource(Users, "/users")

class UsersById(Resource):
    def get(self, id):
        user = User.query.filter_by(id = id).one_or_none()
        if user is None:
            return make_response({"error" : "User does not exist"}, 404)
        
        return make_response(user.to_dict(), 200)

    def patch(self, id):
        try:
            user = User.query.filter_by(id = id).one_or_none()
            if user is None:
                return make_response({"error" : "User does not exist"}, 404)
            request_json = request.get_json()
            for key in request_json:
                setattr(user, key, request_json[key])
            db.session.add(user)
            db.session.commit()
            return make_response(user.to_dict(), 200)
        except:
            return make_response({"error" : "PATCH UserById"}, 404)

api.add_resource(UsersById, "/users/<int:id>")

class Signup(Resource):
    def post(self):
        request_json = request.get_json()

        user_name = request_json.get("username")
        password = request_json.get("password")

        user_ids = [user.user_id for user in User.query.all()]
        print("these are the user_id's : " + str(user_ids))
        unique_id = ""

        print(request_json)

        while (True):
            random_id = uuid.uuid1()
            if random_id:
                if random_id not in user_ids:
                    unique_id = random_id
                    break
            else:
                print("Failed to make a random id, retrying...")
                continue

        print("THIS IS THE UNIQUE ID : " + str(unique_id))
        print("this is the type of the user_id : " + str(type(unique_id)))
        
        user = User(
            username = user_name,
            image_url = "https://miro.medium.com/v2/resize:fit:1200/1*qzR_zFHUtlkbNkAuk2IVPQ.jpeg",
            user_id = str(unique_id),
            points = 300,
            total_points = 0
        )

        print(user)

        user.password_hash = password

        db.session.add(user)
        # this is the problem
        # session["userId"] = user.user_id
        # session["user"] = user
        session["user_id"] = user.id
        db.session.commit()

        return make_response(user.to_dict(), 201)

api.add_resource(Signup, "/signup", endpoint="signup")

class Login(Resource):
    def post(self):
        request_json = request.get_json()

        user_name = request_json.get("username")
        password = request_json.get("password")


        user = User.query.filter(User.username == user_name).first()
        print(user)
        if user:
            if user.authenticate(password):

                # Create sessions for every attribute of user
                # session["userId"] = user.user_id
                # session["user"] = user
                session["user_id"] = user.id
                return make_response(user.to_dict(), 200)
            
            return make_response({"error" : "401 Unauthorized"}, 401)

api.add_resource(Login, "/login", endpoint="login")


# ENDPOINTS FOR ICONS

# This gets all the icons
class Icons(Resource):
     def get(self):
         icons = [icon.to_dict() for icon in Icon.query.all()]
         return make_response(icons, 200)
    
api.add_resource(Icons, "/icons")

# Create icons here
# This one just gets all the icons that the user owns
class UserIconsById(Resource):
    def get(self, id):
        # I think I just fixed
        # I need to get the session of the user and their user.id not user_id
        # Because user.id and user_id are two different things
        # user_id is the thing you added for random id's
        user_id = session["user_id"]

        user_icons = UserIcon.query.filter_by(user_id=id).all()
        user_icons_dicts = [icon.to_dict() for icon in user_icons]
        return make_response(jsonify(user_icons_dicts), 200)

api.add_resource(UserIconsById, "/usericons/<int:id>")

# This creates a relationship between the user and a specific icon that is bought
class UserIconPost(Resource):
    def post(self):
        try:
            request_json = request.get_json()

            newUserIcon = UserIcon(
                icon_id = request_json["icon_id"],
                user_id = request_json["user_id"]
            )

            db.session.add(newUserIcon)
            db.session.commit()

            return make_response(newUserIcon.to_dict(), 200)
        except:
            return make_response({"error" : "POST UserIcon"}, 404)
        
api.add_resource(UserIconPost, "/usericons")

# Write me a code that gets UserIcons that are specific to the user_id.

class Tags(Resource):
    def get(self):
        tags = [tag.to_dict() for tag in Tag.query.all()]
        return make_response(tags, 200)

api.add_resource(Tags, "/tags")

class UserTagById(Resource):
    def get(self, id):
        user_tags = UserTag.query.filter_by(user_id=id).all()
        user_tag_dicts = [tag.to_dict() for tag in user_tags]
        return make_response(jsonify(user_tag_dicts), 200)
    
api.add_resource(UserTagById, "/usertags/<int:id>")

class UserTagPost(Resource):
    def post(self):
        try:
            request_json = request.get_json()

            newUserTag = UserTag(
                tag_id = request_json["tag_id"],
                user_id = request_json["user_id"]
            )

            db.session.add(newUserTag)
            db.session.commit()

            return make_response(newUserTag.to_dict(), 200)
        except:
            return make_response({"error" : "POST UserIcon"}, 404)
    
api.add_resource(UserTagPost, "/usertags")


@socketio.on('back_button')
def handle_back_button(data):
    handle_disconnect()
    print(str(players_in_games))

@socketio.on('connect')
def handle_connect(socket):
    sid = request.sid
    print(f"{sid} Just connected on server side")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    print(f"{sid} disconnected")
    if players_in_games.get(sid, None):
        print("player was in game so need place player in disconnected players and switch game hosts if host...")
        room = players_in_games[sid][0]
        user_id = players_in_games[sid][1]
        game = game_rooms.get(room, None)
        leave_room(room)
        if game:
            # print("putting in disconnected players...")
            # game["disconnected_players"][user_id] = True
            # del players_in_games[sid]
            if game["total_players"] == 1:
                print("deleting room")
                del game_rooms[room]
                del players_in_games[sid]
            elif game["game_started"] == False:
                default_player_dict = {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, 
                                       "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, 
                                       "pregame": 0, "sid": ""}
                this_player = game["player_map"][user_id]
                curr_host = game["host"]

                game["disconnected_players"][user_id] = True
                game["total_players"] -=1
                del players_in_games[sid]
                game["player_data"][this_player] = default_player_dict
                del game["player_map"][user_id]
                game["player_ids"].remove(user_id)
                socketio.emit("player_left", {"game": game}, room = room)
            elif game["game_started"] and game["player_cards_dealt"] == False:
                #first gap
                if user_id == game["host"]:
                    #run the host logic otherwise just regular disconnect
                    curr_host = game["host"]
                    game["host"] = ""
                    #Temporarily blanking out host will quickly assign
                    print("putting in disconnected players...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]
                    for player in game["player_order"]:
                        player_data = game["player_data"][player]
                        player_id = player_data["userId"]
                        if game["disconnected_players"].get(player_id, None) == None and player_id is not curr_host:
                            game["host"] = player_id
                            break
                    print("reassigning host at turn gap interval....")
                    socketio.emit("reassign_host", {"new_host": game["host"]}, room = room)
                else:
                    #Not host run regular disconnect logic
                    print("regular disconnect...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]

            elif game["flop_dealt"] == False and game["pregame_bets_completed"]:
                if user_id == game["host"]:
                    #run the host logic otherwise just regular disconnect
                    curr_host = game["host"]
                    game["host"] = ""
                    #Temporarily blanking out host will quickly assign
                    print("putting in disconnected players...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]
                    for player in game["player_order"]:
                        player_data = game["player_data"][player]
                        player_id = player_data["userId"]
                        if game["disconnected_players"].get(player_id, None) == None and player_id is not curr_host:
                            game["host"] = player_id
                            break
                    print("reassigning host at turn gap interval....")
                    socketio.emit("reassign_host", {"new_host": game["host"]}, room = room)
                else:
                    #Not host run regular disconnect logic
                    print("regular disconnect...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]

            elif game["turn_dealt"] == False and game["flop_bets_completed"]:
                #This should be right in between betting and emitting turn
                #IF host caught disconnnecting here need to swap host
                #When reconnecting player emit new host...need to see if enough time
                # to get code through
                if user_id == game["host"]:
                    #run the host logic otherwise just regular disconnect
                    curr_host = game["host"]
                    game["host"] = ""
                    #Temporarily blanking out host will quickly assign
                    print("putting in disconnected players...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]
                    for player in game["player_order"]:
                        player_data = game["player_data"][player]
                        player_id = player_data["userId"]
                        if game["disconnected_players"].get(player_id, None) == None and player_id is not curr_host:
                            game["host"] = player_id
                            break
                    print("reassigning host at turn gap interval....")
                    socketio.emit("reassign_host", {"new_host": game["host"]}, room = room)
                else:
                    #Not host run regular disconnect logic
                    print("regular disconnect...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]
                
            elif game["river_dealt"] == False and game["turn_bets_completed"]:
                if user_id == game["host"]:
                    curr_host = game["host"]
                    game["host"] = ""
                    #Temporarily blanking out host will quickly assign
                    print("putting in disconnected players...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]
                    for player in game["player_order"]:
                        player_data = game["player_data"][player]
                        player_id = player_data["userId"]
                        if game["disconnected_players"].get(player_id, None) == None and player_id is not curr_host:
                            game["host"] = player_id
                            break
                    print("reassigning host at river gap interval....")
                    socketio.emit("reassign_host", {"new_host": game["host"]}, room = room)
                else:
                    #Not host run regular disconnect logic
                    print("regular disconnect...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]
                
            elif game["winners_declared"] == False and game["river_bets_completed"]:
                #This is the gap after river bets completed betting round has ended and
                #Check win needs to run but may have slight delay
                if user_id == game["host"]:
                    curr_host = game["host"]
                    game["host"] = ""
                    #Temporarily blanking out host will quickly assign
                    print("putting in disconnected players...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]
                    for player in game["player_order"]:
                        player_data = game["player_data"][player]
                        player_id = player_data["userId"]
                        if game["disconnected_players"].get(player_id, None) == None and player_id is not curr_host:
                            game["host"] = player_id
                            break
                    print("reassigning host at point where winners will be declared....")
                    socketio.emit("reassign_host", {"new_host": game["host"]}, room = room)
                else:
                    #Not host run regular disconnect logic
                    print("regular disconnect...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]

            elif game["winners_declared"] and game["player_cards_dealt"] == True:
                #Winners were declared but restart has not occurred it hasn't ran
                #This is a gap point so swap hosts if host exits at this time
                if user_id == game["host"]:
                    curr_host = game["host"]
                    game["host"] = ""
                    #Temporarily blanking out host will quickly assign
                    print("putting in disconnected players...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]
                    for player in game["player_order"]:
                        player_data = game["player_data"][player]
                        player_id = player_data["userId"]
                        if game["disconnected_players"].get(player_id, None) == None and player_id is not curr_host:
                            game["host"] = player_id
                            break
                    print("reassigning host at point where winners will game will be reset....")
                    socketio.emit("reassign_host", {"new_host": game["host"]}, room = room)
                else:
                    #Not host run regular disconnect logic
                    print("regular disconnect...")
                    game["disconnected_players"][user_id] = True
                    game["total_players"] -=1
                    del players_in_games[sid]
            else:
                #Regular disconnect no need to swap host
                print("regular disconnect will not swap host")
                game["disconnected_players"][user_id] = True
                game["total_players"] -=1
                del players_in_games[sid]





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
        game = game_rooms[room]
        #old model before 2/28 ---------------
        if userId not in game["player_ids"] and len(game_rooms.get(room)["player_ids"]) < 6 and game["game_started"] == False:
            #THIS RUNS IF GAME EXISTS AND NEW PLAYER JOINING AND IS NOT FULL OF PLAYERS....maybe add if not game started....
            #Maybe add one more condition to ensure game hasn't started and handle other conditions elsewhere...
            #Look through game for available player seats, if seat is available user is assigned this player/seat ----
            # game = game_rooms[room]
            player_data = game["player_data"]
            if player_data["player1"]["userId"] == "":
                #add the player here
                game["total_players"] +=1
                players_in_games[request.sid] = [room, userId, request.sid]
                print("new player has joined the room")
                player_data["player1"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 2000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                # game["player_order"].append("player1")
                game["player_map"][userId] = "player1"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"]}, room = room )
                
            elif player_data["player2"]["userId"] == "":
                game["total_players"] +=1
                players_in_games[request.sid] = [room, userId, request.sid]
                print("new player has joined the room")
                player_data["player2"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                # game["player_order"].append("player2")
                game["player_map"][userId] = "player2"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"]}, room = room )
                
            elif player_data["player3"]["userId"] == "":
                game["total_players"] +=1
                players_in_games[request.sid] = [room, userId, request.sid]
                print("new player has joined the room")
                player_data["player3"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                # game["player_order"].append("player3")
                game["player_map"][userId] = "player3"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"]}, room = room )
                
            elif player_data["player4"]["userId"] == "":
                game["total_players"] +=1
                players_in_games[request.sid] = [room, userId, request.sid]
                print("new player has joined the room")
                player_data["player4"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                # game["player_order"].append("player4")
                game["player_map"][userId] = "player4"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"]}, room = room )
                
            elif player_data["player5"]["userId"] == "":
                game["total_players"] +=1
                players_in_games[request.sid] = [room, userId, request.sid]
                print("new player has joined the room")
                player_data["player5"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                # game["player_order"].append("player5")
                game["player_map"][userId] = "player5"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"]}, room = room )

            elif player_data["player6"]["userId"] == "":
                game["total_players"] +=1
                players_in_games[request.sid] = [room, userId, request.sid]
                print("new player has joined the room")
                player_data["player6"] = {"user": user, "userId": userId, "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid}
                game["player_ids"].append(userId)
                # game["player_order"].append("player6")
                game["player_map"][userId] = "player6"
                socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"]}, room = room )
        elif game["player_map"].get(userId, None) == None and len(game_rooms.get(room)["player_ids"]) < 6 and game["game_started"] == True:
            #Was not in game but game is not full and so can join it remember to make edge case for full game
            pass
        elif game["game_started"] == True and game["player_map"].get(userId, None):
            #IF GAME EXISTS AND PLAYER IS IN THE LIST OF PLAYERS THEY CAN JUST REJOIN IF IN SAME ROUND
            print(f"{user} is rejoining an existing game...")
            game = game_rooms[room]
            
            
            round = game["betting_round"]
            print(f"The round is {round}")
            print(game[round + "_bets_taken"])

            players_in_games[request.sid] = [room, userId, request.sid]
            player = game["player_map"][userId]
            player_cards = game["player_data"][player]["cards"]
            player_money = game["player_data"][player]["cash"]
            game["total_players"] +=1

            #remove from disconnected players
            print("disconnected players prior to removing rejoining player" + str(game["disconnected_players"]))
            del game["disconnected_players"][userId]

            min_bet_difference = game["min_bet"] - game["player_data"][player][round]
            #ALLOW PLAYER TO REJOIN TO THEIR PROPER STAGE WITHIN THE GAME
            #MAY WANT TO SET GAME TO FALSE AT START ON BACKEND THEN WITH STARTING SET TO TRUE
            if game["game_started"] and game["player_cards_dealt"] == False:
                print("player will be returned to game with their data recovered")
                socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room )

            elif game["pregame_bets_taken"] == True and game["pregame_bets_completed"] == False:
                if game["round_order"][game["current_turn"]] == player:
                    print(f"letting {user} bet again")
                    socketio.emit('rejoin_at_bet',{"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room)
                else:
                    print("player will be returned to game with their data recovered")
                    socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room )
            
            elif game["game_started"] and game["flop_dealt"] == False:
                print("player will be returned to game with their data recovered")
                socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room )
            
            elif game["pregame_bets_completed"] and game["flop_bets_taken"] and game["flop_bets_completed"] == False:
                if game["round_order"][game["current_turn"]] == player:
                    print(f"letting {user} bet again")
                    socketio.emit('rejoin_at_bet',{"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room)
                else:
                    print("player will be returned to the flop betting with their data recovered, but it is not yet their turn")
                    socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room )
            
            elif game["game_started"] and game["turn_dealt"] == False:
                print("player will be returned to game with their data recovered")
                socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room )
            
            elif game["flop_bets_completed"] and game["turn_bets_taken"] and game["turn_bets_completed"] == False:
                if game["round_order"][game["current_turn"]] == player:
                    print(f"letting {user} bet again")
                    print(game["all_player_cards"])
                    socketio.emit('rejoin_at_bet',{"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room)
                else:
                    print("player will be returned to the flop betting with their data recovered, but it is not yet their turn")
                    socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room )
            
            elif game["game_started"] and game["river_dealt"] == False:
                print("player will be returned to game with their data recovered")
                print("river cards should be dealt out directly after?")
                socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room )
            
            elif game["turn_bets_completed"] and game["river_bets_taken"] and game["river_bets_completed"] == False:
                if game["round_order"][game["current_turn"]] == player:
                    print(f"letting {user} bet again")
                    print(game["all_player_cards"])
                    socketio.emit('rejoin_at_bet',{"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room)
                else:
                    print("player will be returned to the flop betting with their data recovered, but it is not yet their turn")
                    socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room )
            else:
                #TRYING TO IMPLEMENT THIS AS RETURNING AT ANY OTHER POINT
                print(f"player: {user} will be returned to the flop betting with their data recovered, but just standard in between actions..")
                socketio.emit('rejoin_game', {"game": game, "user": userId, "player_cash": player_money, "bet_difference": min_bet_difference, "time": game["time"] }, room = room )
    else:
        print("host is creating a room...")
        game_rooms[room] = {
            "id": room,
            "host": userId,
            "game_started": False,
            "total_players": 1,
            "player_map": {userId: "player1"},
            "player_data": {"player1": {"user": user, "userId": userId, "cards": ["", ""], "cash": 2000, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": request.sid},
                            "player2": {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": ""},
                            "player3": {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": ""},
                            "player4": {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": ""},
                            "player5": {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": ""},
                            "player6": {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": ""}},

            "all_player_cards": ["player1", "player2", "player3", "player4", "player5", "player6"],
            "table_cards": [],
            "deck": [],
            "last_card_dealt": 0,
            "player_ids": [userId],
            "player_order": ["player1", "player2", "player3", "player4", "player5", "player6"],
            "round_order": [],
            "first_better": "",
            "current_turn": 0,
            "turn_number": 0,
            "player_cards_dealt": False,
            "player_cards_dealing": False,
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
            "small_blind_bet": "",
            "big_blind_bet": "",
            "time": 15,
            #----------------------
            "disconnected_players": {},
            "betting_index": 0,
            "winners_declared": False,
            "winners": [],
            "game_over": False
        }
        players_in_games[request.sid] = [room, userId, request.sid]
        game = game_rooms[room]

        socketio.emit("add_player", {"player_data": game["player_data"], "all_player_cards": game["all_player_cards"]}, room = room )
    # print(game_rooms.get(room))
    # print("User was added or rejoined a room")
    # print(players_in_games)

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
    
    game["game_started"] = True
    print("--------------------------------------------------------------------------------------------------------------------------------")
    print("\nserver letting players know game is starting...and shuffling deck")
    print("this is the first card in the deck to confirm")
    print(data["deck"][0])
    print("\n")

    #------------------------------------------------------------
    if game["disconnected_players"].get(game["host"], None):
        #if host in disconnected players fix this
        #possibly make this into function to re use? 
        curr_host = game["host"] 
        game["host"] = ""
        for player in game["player_order"]:
            player_data = game["player_data"][player]
            player_id = player_data["userId"]
            if player_id and game["disconnected_players"].get(player_id, None) == None and player_id is not curr_host:
                game["host"] = player_id
                print("assigned this person as host " + player_id)
                break
        print("reassigning host since not present at game start....")
        print("this is the new host: " + game["host"])
    #---------------------------------------------------------------
    game["betting_round"] = "pregame"
    socketio.emit('starting', game, room = room)

@socketio.on('deal_cards')
def deal_cards(data):
    print("\ndeal cards is running....")
    room = data["room"]
    
    
    # cards = data["cards"]
    game = game_rooms.get(room)
    cards = game["deck"]
    cards_dealt = game["player_cards_dealt"]
    if not cards_dealt:
        game["player_cards_dealing"] = True
        game["player_cards_dealt"] = True
        game["betting_round"] = "pregame"
        print("player order in dealing cards")
        print(game["player_order"])
        for player in game["player_order"]:
            #player1, player2...
            player_data = game["player_data"][player]
            player_id = player_data["userId"]
            player_cash = player_data["cash"]

            # game["current_turn"] = player_name
            #Making sure player has enough money to play as well as if player object is being occupied aka not empty
            if player_id and player_cash > 0: 
                game["round_order"].append(player)
                player_data["cards"] = []
                player_data["cards"].append(cards[game["last_card_dealt"]])
                player_data["cards"].append(cards[game["last_card_dealt"] + 1])

            #adding in security so game at player cards dealt is only set to true once last set of cards have been emitted
            game["last_card_dealt"] += 2
            #Is this a burn card? if so we can remove, no cards need be removed at this point
            game["last_card_dealt"] += 1

        #Small blind logic plus checking else case if total players in round order is less than 2
        if len(game["round_order"]) > 1:

            #Assign first player in order impoortant for keeping order at end of game
            game["first_better"] = game["round_order"][0]
            small_blind = game["round_order"][- 2]
            big_blind = game["round_order"][- 1]

            print("THIS IS THE SMALL BLIND : " + str(small_blind))
            print("THIS IS THE BIG BLIND : " + str(big_blind))

            small_blind_data = game["player_data"][small_blind]
            small_blind_cash = game["player_data"][small_blind]["cash"]
            big_blind_data = game["player_data"][big_blind]
            big_blind_cash = game["player_data"][big_blind]["cash"]

            small_blind_bet = ""
            big_blind_bet = ""

            if small_blind_cash <= 5:
                print("small blind does not have enough to meat sb so is all in")
                small_blind_data["cash"] -= small_blind_cash
                small_blind_data["pregame"] += small_blind_cash
                small_blind_bet = small_blind_cash
                small_blind_data["status"] = "all_in"

                game["small_blind_bet"] = small_blind_cash

                game["players_all_in"].append(small_blind)
                game["min_bet"] = small_blind_cash
                print("\n Small blind cash is " + str(small_blind_cash))
                game["min_all_in"].append(small_blind_cash)
                game["pots"].append({"cash" : 0, "players" : []})
                game["bets"].append({"player_name" : small_blind, "bet" : small_blind_cash})
            else:
                small_blind_data["cash"] -= 5
                small_blind_data["pregame"] += 5
                small_blind_bet = 5

                game["small_blind_bet"] = 5

                game["min_bet"] = 5
                game["bets"].append({"player_name" : small_blind, "bet" : 5})

            if big_blind_cash <= 10:
                print("big blind does not have enough to meat bb so is all in")
                big_blind_data["cash"] -= big_blind_cash
                big_blind_data["pregame"] += big_blind_cash
                big_blind_bet = big_blind_cash
                big_blind_data["status"] = "all_in"

                game["big_blind_bet"] = big_blind_cash

                game["players_all_in"].append(big_blind)

                # if (big_blind_cash != game["min_bet"]):
                #UNCOMMENT ABOVE IF ISSUES ARISE 3/8 and tab over if statement below
                if (big_blind_cash not in game["min_all_in"]):
                    game["min_all_in"].append(big_blind_cash)
                    game["pots"].append({"cash" : 0, "players" : []})
                if big_blind_cash > game["min_bet"]:
                    game["min_bet"] = big_blind_cash
                print("\n Big blind cash is " + str(big_blind_cash))
                game["bets"].append({"player_name" : big_blind, "bet" : big_blind_cash})
            else:
                big_blind_data["cash"] -= 10
                big_blind_data["pregame"] += 10
                big_blind_bet = 10
                game["big_blind_bet"] = 10
                game["min_bet"] = 10
                game["bets"].append({"player_name" : big_blind, "bet" : 10})

            if len(game["round_order"]) == 2 and big_blind_bet == small_blind_bet and small_blind_cash <= 5:
                print("edge case handling BB matches SB and is all in...SB is also all in...")
                #EDGE CASE HANDLING -----------------
                #big blind had exactly 5 dollars and matched small blind then went all in
                #Both players are done betting since there are only two and bets are equal
                #No betting is done so doesnt run through bet assignment system so just assigning pot value here
                game["pot"] = small_blind_bet + big_blind_bet
            elif len(game["round_order"]) == 2 and big_blind_bet == small_blind_bet:
                print("Edge case handling BB matches SB and is all in but SB is not all in, however only 2 players so will not route back")
                #EDGE CASE HANDLING ------------------------------
                game["pot"] = small_blind_bet + big_blind_bet


            print("THESE ARE THE PLAYERS CASH AFTER BLINDS : ")
            print(game["player_data"][small_blind])
            print(game["player_data"][big_blind])

            print("THIS IS THE MIN BET NOW : " + str(game["min_bet"]))    
            print("THIS IS THE MAIN POT AFTER BLINDS : " + str(game["pot"])) 

            # place_pot_bets(game)

            #3/5
            # When emitting this because of blinds you will want to send the amount from the blinds directly...it will not persist but just to show blinds...
            socketio.emit("dealing", {"adding_cards": game["player_data"],"player_cards_dealt": game["player_cards_dealt"], "dealing": game["player_cards_dealing"]}, room = room)
        else:
            print("emit something that stops flow of game and set game start to false...not enough players to play a round...")
            pass


@socketio.on("deal_flop")
def deal_flop(data):
    print("\ndealing the flop...")
    
    room = data["room"]
    game = game_rooms.get(room)
    cards = game["deck"]
    if not game["flop_dealt"]:
        game["flop_dealt"] = True
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
        socketio.emit("dealing_flop", {"table_cards": game["table_cards"], "dealt": True}, room = room)
        
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
        print("this is the startin player")
        player = game["round_order"][starting_player]
        print(game["round_order"])
        #player1 or player2 or ....etc
        player_data = game["player_data"][player]
        player_status = player_data["status"]

        if (len(game["round_order"]) - len(game["players_folded_list"]) <= 1):
            #ALL BUT ONE PLAYER HAS FOLDED NO MORE BETTING WINNER CAN NOW BE DECLARED
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

            #capturing special edge case below of bigblind not having enough and forcing all in but player 1 still has to match their bet. only 2 players
            #Example of above player 2 is bb and all in with 8, player 1 must put in 3 more to match...
            if player_data["status"] != "all_in" and round == "pregame" and player_data["pregame"] < game["min_bet"]:
                print("special edge case occurring....this player is player 1 and must bet once more...")

                min_bet_difference = game["min_bet"] - game["player_data"][player][round]
                current_bet_id = game["betting_index"]
                user_id = game["player_data"][player]["userId"]
                player_bankroll = game["player_data"][player]["cash"]
                game["player_data"][player]["myTurn"] = True
                game[round + "_bets_taken"] = True


                #SOLUTION TO TIMING OUT
                game["time"] = 30
                current_bet_id = game["betting_index"]

                socketio.emit("take_bet", {"game_update": game, "player_cash": player_bankroll, "user": user_id, "bet_difference": min_bet_difference, "time": game["time"]}, room = room)
                while game["time"] >= -3:
                    print(game["time"])
                    if game["betting_index"] != current_bet_id:
                        break
                    elif game["time"] == -3:
                        auto_fold(room, player)
                        # print("OUT OF TIME EXECUTE FUNCTION!!! CLOSE BETTING!")
                        break
                    else:
                        game["time"] -=1
                        time.sleep(1)
            else:

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
                    starting_player = game["current_turn"]
                    player = game["round_order"][starting_player]
                    player_data = game["player_data"][player]
                    if player_data["status"] == "fold":
                        game["current_turn"] +=1
                    elif player_data["status"] == "all_in":
                        game["current_turn"] +=1
                    else:
                        break

            if game["current_turn"] == len(game["round_order"]):
                print("Betting has ended we need to comm with front end")
                game[round + "_bets_completed"] = True
                game[round + "_bets_taken"] = True
                reset_betting(room, game)
                socketio.emit("end_betting_round", {"game_update": game}, room = room)
            else:
                min_bet_difference = game["min_bet"] - game["player_data"][player][round]

                current_bet_id = game["betting_index"]
                user_id = game["player_data"][player]["userId"]
                player_bankroll = game["player_data"][player]["cash"]
                game["player_data"][player]["myTurn"] = True

                #SOLUTION TO TIMING OUT
                game["time"] = 30
                game["betting_index"] = 0
                current_bet_id = game["betting_index"]

                game[round + "_bets_taken"] = True
                socketio.emit("take_bet", {"game_update": game, "player_cash": player_bankroll, "user": user_id, "bet_difference": min_bet_difference, "time": game["time"]}, room = room)
                #p2 of timing out...
                while game["time"] >= -3:
                    print(game["time"])
                    if game["betting_index"] != current_bet_id:
                        break
                    elif game["time"] == -3:
                        auto_fold(room, player)
                        # print("OUT OF TIME EXECUTE FUNCTION!!! CLOSE BETTING!")
                        break
                    else:
                        game["time"] -=1
                        time.sleep(1)
    
@socketio.on("handle_bet_action")
def handle_bet_action(data):
   
    room = data["room"]
    game = game_rooms.get(room)

    user_id = data["userId"]
    user_name = data["user"]

    player_name = game["player_map"][user_id]

    status = data["bet_status"]
    bet_amount = int(data["bet"])
    player_data = game["player_data"][player_name]
    #This turns off my turn for player ---if presenting problems can also do this right after take bet occurs... review this for deletion
    game["player_data"][player_name]["myTurn"] = False
    round = game["betting_round"]

    #REQUIRED FOR GAME TIMER
    game["time"] = 30
    game["betting_index"] += 1

    print("\nThis is the player that just had an opportunity to bet, their data is being received")
    print(player_name)
    print(f"This player's betting status is {status}.....\n")
    print("THIS IS THE BET AMOUNT : " + str(bet_amount))


    player_data[round] += bet_amount
    game["player_data"][player_name]["cash"] -= bet_amount


    total_bet_amount = player_data[round]

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

       
    #-------------------------------------------------------------------------------------
    if status == "all_in":
        player_data["status"] = "all_in"
        game["players_all_in"].append(player_name)
        #Added if conditon here 2/17 to allow cycle back if the all in is the only raise
        if total_bet_amount > game["min_bet"]:
            game["last_raise"] = player_name
            game["raise_occurred"] = True
            print("There was an all in raise....")
        if (total_bet_amount != game["min_bet"]):
            if (bet_amount not in game["min_all_in"]):
                game["min_all_in"].append(total_bet_amount)
                game["pots"].append({"cash" : 0, "players" : []})
        elif (round == "pregame" and total_bet_amount == game["min_bet"] and game["min_bet"] == game["big_blind_bet"] ):
            #ELIF round is pregame and total bet is equal to min bet and min bet is BB added 3/7
            #NEWW 3/7 Captures special small blind edge case they had 10 dollars put 5 dollar big blind and only have 5 left, forced by BB to go all in
            #NEED TO CREATE SPLIT FOR THIS PERSON THAT OTHERWISE WOULD NOT OCCUR
            if (bet_amount not in game["min_all_in"]):
                game["min_all_in"].append(total_bet_amount)
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


    if total_bet_amount > game["min_bet"]:
        game["min_bet"] = total_bet_amount

    #CHECK IF NEXT PLAYER IS ALL IN OR HAS FOLDED IF SO SKIP THEM AND INCREMENT AGAIN
   
    while game["current_turn"] < len(game["round_order"]):
        next_player = game["round_order"][game["current_turn"]]
        next_player_data = game["player_data"][next_player]
        if next_player_data["status"] == "fold":
            game["current_turn"] +=1
        elif next_player_data["status"] == "all_in":
            #NEWWW 3/6 previously just incremented currrent turn by 1
            if next_player == game["last_raise"]:
                print(f"{next_player} went all in and was also last to raise prepare to stop betting here")
                game["current_turn"] = len(game["round_order"])
            else:
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
            #ALL BUT ONE PLAYER HAS FOLDED NO MORE BETTING WINNER CAN NOW BE DECLARED, no need to cycle again
            print("IS THIS RUNNING FOR SOME REASON???")
            game["current_turn"] = len(game["round_order"])
            game["raise_occurred"] = False

        print("running restart betting round since someone raised \n")
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
        print("Betting has ended we need to comm with front end")
        game[round + "_bets_taken"] = True
        game[round + "_bets_completed"] = True


        # # --------------- POT LOGIC ---------------

        accrued_round_bets = []
        for player in game["round_order"]:
            print("\n organizing round bets for round:  " + round)
            bets_this_round = game["player_data"][player][round]
            accrued_round_bets.append({"player_name": player, "bet": bets_this_round}) 
        #REASSIGNMENT OF BETS
        game["bets"] = accrued_round_bets
        print("\n Fixing bets.....")
        print(game["bets"])
        print("\n")

        # If small pots exists
        if (len(game["pots"]) > 0):
            
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

        else:
            for i in range(len(game["bets"])):
                    print("This is the main pot: " + str(game["pot"]))
                    print("This is how much is getting added: " + str(game["bets"][i]["bet"]))
                    game["pot"] += game["bets"][i]["bet"]
                    print("This is the main pot after getting added: " + str(game["pot"]))
                    print("\n")
                    print("\n")

        # --------------- POT LOGIC ---------------

        print("These are the pots " + str(game["pots"]))
        print("This is min all in" + str(game["min_all_in"]))
        print("These are the bets" + str(game["bets"]))
        print("This is the main pot " + str(game["pot"]))
        game["bets"] = []
        game["min_all_in"] = []

        print("Emitting to the game...checking who was host: ")
        print(game["host"])
        reset_betting(room, game)
        print("Emitting to the game...checking who is host: ")
        print(game["host"])
        socketio.emit("end_betting_round", {"game_update": game}, room = room)
        print("The betting round has ended \n")
    else:
        #still more players to cycle through original betting round
        continue_betting(room, game)
        pass

@socketio.on("check_win")
def winner_winner_chicken_dinner(data):
    room = data["room"]
    game = game_rooms.get(room)
    
    if game["winners_declared"] == False:
        game["winners_declared"] = True
        print("declaring winners still runs even with the caviot above...") 
        players_not_playing = []
        print("THESE ARE THE POTS BEFORE REMOVING EMPTY SIDE POTS : " + str(game["pots"]))

        for player in game["players_folded_list"]:
            players_not_playing.append(player)

        # Removing any empty pots that are still remaining
        for i in range(len(game["pots"])):
            if len(game["pots"][i]["players"]) == 0 and game["pots"][i]["cash"] == 0:
                game["pots"].pop(i)
        
        print("THESE ARE THE SIDE POTS AFTER REMOVING EMPTY SIDE POTS : " + str(game["pots"]))

        # for player in game["players_folded_list"]:
        #     players_not_playing.append(player)

        if (len(game["pots"]) > 0):
            print("SINCE THERE ARE SMALL POTS WE WILL RUN THOSE SMALL POTS FIRST")
            while (len(game["pots"]) > 0):
                # getting the active pot
                pot_in_play = game["pots"][len(game["pots"]) - 1]
                print("THIS IS THE POT IN PLAY RIGHT NOW : " + str(pot_in_play))
                players_playing = {}


                #NEWWWW 3/6
                if len(game["pots"]) -1 != 0:
                    #NOT THE LAST POT WHICH NEEDS SPECIAL CONDITION TO MOVE MONEY TO MAIN POT
                    next_pot = game["pots"][len(game["pots"]) - 2]
                    if pot_in_play["players"] == next_pot["players"]:
                        #pot has the same players as next pot so combine pots and erase this one
                        next_pot["cash"] += pot_in_play["cash"]
                        game["pots"].pop()
                        continue
                        

                # Getting all the players that can be in play of the active pot
                #Sergio NEED change to eman game 2/28 ------------- change game at player data to game at round order...
                for player_name in game["round_order"]:
                    if player_name in pot_in_play["players"] and player_name not in players_not_playing:
                        players_playing[player_name] = game["player_data"][player_name]

                print("THESE ARE THE PLAYERS PLAYING IN THE POT IN PLAY : " + str(players_playing))

                #NEWWWW 3/6
                if list(players_playing.keys()) == []:
                    print("no players in pot so move money down one")
                    if len(game["pots"]) -1 != 0:
                        next_pot = game["pots"][len(game["pots"]) - 2]
                        next_pot["cash"] += pot_in_play["cash"]
                        game["pots"].pop()
                        continue
                    elif len(game["pots"]) -1 == 0:
                        game["pot"] += pot_in_play["cash"]
                        game["pots"].pop()
                        continue
                


                # Gets the winning players as a list
                winning_players = determine_winner(game, players_playing)
                game["winners"].append(winning_players)
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

                # print("THESE ARE THE PLAYERS BEFORE CASH EARNINGS WON : " + str(game["player_data"]))

                # Distributing the prize earnings from pot evenly to the winning players
                #Made change here on 3/1 changed player data to round order
                for player in game["round_order"]:
                    if player in winning_players:
                        game["player_data"][player]["cash"] += pot_in_play["cash"] // len(winning_players)

                print("THESE ARE THE PLAYERS AFTER CASH EARNINGS WON : " + str(game["player_data"]))
                print("\n\n")

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
            game["winners"].append(winning_players)
            print("THESE ARE THE WINNERS OF THE MAIN POT : " + str(winning_players))

            print("THIS IS THE AMOUNT THE MAIN POT HAS : " + str(game["pot"]))

            # print("THESE ARE THE PLAYERS BEFORE EARNINGS : " + str(game["player_data"]))

            # Distributing the earnings from the Main Pot to the winning players
            #Change here as well 3/1 player data swapped to round order
            for player_name in game["round_order"]:
                if player_name in winning_players:
                    game["player_data"][player_name]["cash"] += game["pot"] // len(winning_players)

            print(f"These are the table cards " + str(game["table_cards"]))
            print("THESE ARE THE PLAYERS AFTER EARNINGS : " + str(game["player_data"]))
            print("\n\n")

            game["pot"] = 0
            
            # game["winners_declared"] = True
            print("THESE ARE THE WINNERS BEFORE THE SOCKET : " + str(game["winners"]))
            socketio.emit("returning_winners", {"winners": game["winners"], "game_update": game}, room = room)

        # if no small pots exists then we will just run the main pot
        else:
            print("SINCE THERE ARE NO SMALL POTS WE WILL JUST RUN THE MAIN POT")
            players_playing = {}

            # Adding all players available to play for the main pot
            #Sergio change to eman game 2/28 ------------- change game at player data to game at round order...
            print("SHOW ME WHO FOLDED!")
            print(players_not_playing)
            print("\n")
            for player_name in game["round_order"]:
                if player_name not in players_not_playing:
                    players_playing[player_name] = game["player_data"][player_name]

            print("THESE ARE THE PLAYERS PLAYING : " + str(players_playing))

            # Getting back a list of winning players
            winning_players = determine_winner(game, players_playing)
            game["winners"].append(winning_players)
            print("THESE ARE THE WINNING PLAYERS : " + str(winning_players))

            print("THIS IS THE MAIN POT : " + str(game["pot"]))

            # print("THESE ARE THE PLAYERS BEFORE EARNINGS : " + str(game["player_data"]))

            # Distributing the earnings from the Main Pot to the winning players
            #round order instead of player_data
            for player_name in game["round_order"]:
                if player_name in winning_players:
                    game["player_data"][player_name]["cash"] += game["pot"] // len(winning_players)

            print(f"These are the table cards: " + str(game["table_cards"]))
            print("THESE ARE THE PLAYERS AFTER EARNINGS : " + str(game["player_data"]))
            print("\n\n")

            game["pot"] = 0


            # print(game["winners"])
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

        #SOLUTION TO TIMING OUT
        #TIME IS RESET ABOVE AND BETTING INDEX INCREMENTED ANYTIME BET IS RECEIVED 
        current_bet_id = game["betting_index"]

        socketio.emit("take_bet", {"game_update": game, "player_cash": player_bankroll, "user": user_id, "bet_difference": min_bet_difference, "time": game["time"]}, room = room)
        #p2 of timing out...
        while game["time"] >= -3:
            print(game["time"])
            if game["betting_index"] != current_bet_id:
                break
            elif game["time"] == -3:
                print("AUTO FOLDING")
                auto_fold(room, player)
                # print("OUT OF TIME EXECUTE FUNCTION!!! CLOSE BETTING!")
                break
            else:
                game["time"] -=1
                time.sleep(1)

def auto_fold(room, player):
    game = game_rooms.get(room, None)
    if game:
        print("RAN OUT OF TIME ON BACKEND SO FOLDING FOR PLAYER in AUTO FOLD...")
        print("player who ran out of time is " + player)
        player_data = game["player_data"][player]
        player_id = player_data["userId"]

        if game["disconnected_players"].get(player_id, None):
            print("id was in disconnected ids so emitting fold...")

            if game["disconnected_players"].get(player_id, None):
                #Not only was player disconnected but player was host...
                #Reassignment of host 3/15
                for player_ in game["player_order"]:
                    curr_player_data = game["player_data"][player_]
                    curr_player_id = curr_player_data["userId"]
                    if game["disconnected_players"].get(curr_player_id, None) == None:
                        print("FINDING NEW HOST SHOULD ONLY NEED TO FIND HOST ONCE...")
                        game["host"] = curr_player_id
                        break

            #MAY NEED A CHECK FOR HOST AGAIN?
            #Send userName
            #Send player id
            #send room
            name = game["player_map"][game["host"]]
            print("emitting to " + name)
            socketio.emit("auto_fold", {"host": game["host"], "user": player_data["user"], "userId": player_data["userId"]}, room = room)


def reset_betting(room, game):
    round = game["betting_round"]
    print("\nreseting the betting round")

    game["last_raise"] = ""
    game["raise_occurred"] = False
    # game["betting_round"] = ""
    game["min_bet"] = 0

    #INSERT REASIGNMENT OF HOST LOGIC HERE??? 3/14??------------------
    current_host = game["host"]
    need_new_host = False

    if game["disconnected_players"].get(current_host, None):
        need_new_host = True
        
    for player in game["player_data"]:
        status = game["player_data"][player]["status"]
        user_id = game["player_data"][player]["userId"]
        # print(f"{player}'s status is {status} and this decides if its reset")
        if status != "fold" and status != "all_in":
            # print(f"reseting {player}'s status")
            game["player_data"][player]["status"] = ""
        #PART OF REASIGNMENT OF HOST.......
        if need_new_host:
            if current_host != user_id:
                game_host = user_id
                game["host"] = user_id
                need_new_host = False

    # Moving first player to the back
    first_player = game["round_order"].pop(0)
    game["round_order"].append(first_player)
    game["current_turn"] = 0

def restart_betting_round(room, game):
    game["current_turn"] = 0
    game["raise_occurred"] = False

def start_next_game(room, game):
    default_player_dict = {"user": "", "userId": "", "cards": ["", ""], "cash": 5000, "myTurn": False, "status": "", "flop": 0, "turn": 0, "river": 0, "pregame": 0, "sid": ""}
    
    for player in game["player_data"]:
        player_data = game["player_data"]
        player_data[player]["cards"] = ["", ""]
        player_data[player]["status"] = ""
        player_data[player]["pregame"] = 0
        player_data[player]["flop"] = 0
        player_data[player]["turn"] = 0
        player_data[player]["river"] = 0
        if len(list(game["disconnected_players"].keys())) >= 1:
            if game["disconnected_players"].get(player_data[player]["userId"], None):
                socket_id = player_data[player]["sid"]
                user_id = player_data[player]["userId"]
                #REMOVE PLAYER FROM GAME IN ALL WAYS
                #no need to remove from player order handled further down
                # game["disconnected_players"].remove(user_id)
                game["player_ids"].remove(user_id)

                del game["disconnected_players"][user_id]
                if players_in_games.get(socket_id, None):
                    del players_in_games[socket_id]
                del game["player_map"][user_id]

                player_data[player] = default_player_dict


    # game["all_player_cards"] = []
    game["table_cards"] = []
    game["deck"] = []
    game["last_card_dealt"] = 0
    #NEED TO SET UP PLAYER ORDER that matches original player order at start of round
    #Remove starting player and add to end
    game["round_order"] = []
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

    game["min_all_in"] = []
    game["pots"] = []
    game["bets"] = []
    game["main_pot"] = True
    game["small_blind_bet"] = ""
    game["big_blind_bet"] = ""
    game["time"] = 30

    game["bet_difference"] = False
    game["disconnected_players"] = {}
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


    #move front player in order to the back - old version delete if version below works. 
    # print("this was our player order")
    # print(game["player_order"])
    # game["round_order"] = []
    # first_player = game["player_order"].pop(0)
    # game["player_order"].append(first_player)
    # print(game["player_order"])


    #FIXING PLAYER ORDERS FOR NEXT ROUND...
    #FIRST BETTER BECOMES LAST BETTER IN NEXT GAME
    first_better = game["first_better"]
    full_play_order = ["player1", "player2", "player3", "player4", "player5", "player6",
                        "player1", "player2", "player3", "player4", "player5", "player6"]
    start = full_play_order.index(first_better)
    end = full_play_order.index(first_better, start + 1)
    temp_round_order = full_play_order[start + 1: end]
    temp_round_order.append(first_better)
    final_round_order = []
    for player in temp_round_order:
        #If player object is in use append player to final round order
        #This means these players are still in the game
        if game["player_data"][player]["userId"] != "":
            final_round_order.append(player)
    print("THE FINAL ROUND ORDER!")
    print(final_round_order)
    print("\n")
    game["player_order"] = final_round_order
    print(game["player_order"])




def place_pot_bets(game):
    if (len(game["pots"]) > 0):
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
    "is_straight_flush": 10,
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