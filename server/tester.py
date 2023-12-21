import random
import string

#----------------------------------------------------------
#TESTING CODE GENERATING 
# print(''.join(random.choices(["a", "b", "c"])))
# print(''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + str(random.randint(0,10)), k=15)))

# codes = ["hi", "my", "friends"]
# sent = (" ").join(codes)
# print(sent)


#----------------------------------------------------------
#VERSION CHOSEN FOR Generating random code
# print(''.join(random.choices(string.ascii_letters + string.digits, k=8)))


# def create_code():
#     code = ""

#Keeping Track of player cards ------------------------------
players = {
    "player1": ["A", "2", "5", "6"],
    "player2": ["K", "Q"]
}

for player in players:
    for card in players[player]:
        print(card)

# rooms = {"12": [{"Sergio": []}, {"Eric": []}]}
# cards = [{"A": "Spade"}, {"2": "Spade"}, {"3": "Spade"}, {"4": "Spade"}, {"5": "Spade"}, {"6": "Spade"}, {"7": "Spade"}, {"8": "Spade"}]
# data = {
#     "last_card_positions" : 3
# }
# game_data = {}
# for room in rooms:
#     if room == "12":
#         player_list = rooms[room]
#         card_one_position = data["last_card_positions"]
#         card_two_position = data["last_card_positions"] + 1
#         for player_obj in player_list:
            
#             for user_Name in player_obj:
#                 # game_data["player"] = user_Name
#                 player_obj[user_Name].append(cards[card_one_position])
#                 player_obj[user_Name].append(cards[card_two_position])
#                 print(user_Name)
#                 print(rooms[room])
#             card_one_position +=2
#             card_two_position +=2

game = [{"game1": "100"}, {"game2": "200"}]

game1 = [game[key] for key in game]
# print(game.index("game1"))
print(game1)

#RESTRUCTURING GAME Setup?
#These can also be pulled 
game_rooms = {"id": 12345,
              "player_list" : {
                  "Sergio": [],
                  "James": []
              },
              "table_cards": [],
              "all_cards": [],
              "last_card_dealt": 0,
              
              }

