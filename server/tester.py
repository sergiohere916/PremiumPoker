import random
import string
from itertools import combinations
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

# players = {
#     "player1": ["A", "2", "5", "6"],
#     "player2": ["K", "Q"]
# }

# for player in players:
#     for card in players[player]:
#         print(card)

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

# game1 = [game[key] for key in game]
# # print(game.index("game1"))
# print(game1)

#RESTRUCTURING GAME Setup?
#These can also be pulled 
# game_rooms = [{"id": "GAME1",
#               "player_list" : [{"Sergio": []}, {"Joe": []}],
#               "table_cards": [],
#               "deck": [{"A": "Spade"}, {"2": "Spade"}, {"3": "Spade"}, {"4": "Spade"}, {"5": "Spade"}, {"6": "Spade"}, {"7": "Spade"}, {"8": "Spade"}],
#               "last_card_dealt": 0,
#               "player_order": ["Sergio", "Joe"],
#               "current_turn": "Sergio"
#               },
#               {"id": "GAME2",
#               "player_list" : [{"Steve": []}, {"Jordan": []}],
#               "table_cards": [],
#               "deck": [{"A": "Spade"}, {"2": "Spade"}, {"3": "Spade"}, {"4": "Spade"}, {"5": "Spade"}, {"6": "Spade"}, {"7": "Spade"}, {"8": "Spade"}],
#               "last_card_dealt": 0,
#               "player_order": ["Steve", "Jordan"],
#               "current_turn": "Jordan"
#               },
#               {"id": "GAME3",
#               "player_list" : [{"Michael": []}, {"Gabriel": []}],
#               "table_cards": [],
#               "deck": [{"A": "Spade"}, {"2": "Spade"}, {"3": "Spade"}, {"4": "Spade"}, {"5": "Spade"}, {"6": "Spade"}, {"7": "Spade"}, {"8": "Spade"}],
#               "last_card_dealt": 0,
#               "player_order": ["Michael", "Gabriel"],
#               "current_turn": "Michael"
#               }
#               ]

game_roomss = {
    "GAME1": {
        "id": "GAME1",
        "player_list" : [{"Sergio": []}, {"Joe": []}],
        "table_cards": [],
        "deck": [{"A": "Spade"}, {"2": "Spade"}, {"3": "Spade"}, {"4": "Spade"}, {"5": "Spade"}, {"6": "Spade"}, {"7": "Spade"}, {"8": "Spade"}],
        "last_card_dealt": 0,
        "player_order": ["Sergio", "Joe"],
        "current_turn": "Sergio"
    },
    "GAME2": {
        "id": "GAME2",
        "player_list" : [{"Steve": []}, {"Jordan": []}],
        "table_cards": [],
        "deck": [{"A": "Spade"}, {"2": "Spade"}, {"3": "Spade"}, {"4": "Spade"}, {"5": "Spade"}, {"6": "Spade"}, {"7": "Spade"}, {"8": "Spade"}],
        "last_card_dealt": 0,
        "player_order": ["Steve", "Jordan"],
        "current_turn": "Jordan"
    },
    "GAME3":  {
        "id": "GAME3",
        "player_list" : [{"Michael": []}, {"Gabriel": []}],
        "table_cards": [],
        "deck": [{"A": "Spade"}, {"2": "Spade"}, {"3": "Spade"}, {"4": "Spade"}, {"5": "Spade"}, {"6": "Spade"}, {"7": "Spade"}, {"8": "Spade"}],
        "last_card_dealt": 0,
        "player_order": ["Michael", "Gabriel"],
        "current_turn": "Michael"
    }

}
room = "GAME3"
# #FIND BETTER WAY TO SEARCH OUT SPECIFIC DICT IN A LIST WITHOUT FOR LOOP
# for game in game_rooms:
#     if game["id"] == room:
#         for player_dict in game["player_list"]:
#             for player in player_dict:
#                 game["current_turn"] = player
#                 player_dict[player].append(game["deck"][game["last_card_dealt"]])
#                 player_dict[player].append(game["deck"][game["last_card_dealt"] + 1])
#                 # if len(game["player_order"]) == 
#             game["last_card_dealt"] += 2
#         game["last_card_dealt"] += 1
#         # game["current_turn"] = game["player_order"][game["player_order"].index(game["current_turn"]) + 1]
# print(game_rooms[2]["player_list"])
# print(game_rooms[2]["last_card_dealt"])


# game = game_rooms.get(room)
# for player_dict in game["player_list"]:
#     for player in player_dict:
#         game["current_turn"] = player
#         player_dict[player].append(game["deck"][game["last_card_dealt"]])
#         player_dict[player].append(game["deck"][game["last_card_dealt"] + 1])
#     game["last_card_dealt"] += 2
# game["last_card_dealt"] += 1

# print(game["player_list"])
# print(game["last_card_dealt"])


#SYSTEM FOR CHECKING FOR WINNER ----------------------

# player_cards = [
#     {"name": "A", "suit": "spades", "value": 1},
#     {"name": "A", "suit": "clubs", "value": 1},
# ]

# community_cards = [
#     {"name": "A", "suit": "hearts", "value": 1},
#     {"name": "K", "suit": "diamonds", "value": 13},
#     {"name": "Q", "suit": "spades", "value": 12},
#     {"name": "J", "suit": "clubs", "value": 11},
#     {"name": "10", "suit": "hearts", "value": 10},
# ]

# all_cards = [
#     {"name": "A", "suit": "spades", "value": 1},
#     {"name": "A", "suit": "clubs", "value": 1},
#     {"name": "A", "suit": "hearts", "value": 1},
#     {"name": "K", "suit": "diamonds", "value": 13},
#     {"name": "Q", "suit": "spades", "value": 12},
#     {"name": "J", "suit": "clubs", "value": 11},
#     {"name": "10", "suit": "hearts", "value": 10},
# ]

game_rooms = [{
            "id": 12345,
            "player_list": [{"Sergio": [{"name": "A", "suit": "spades", "value": 1}, {"name": "10", "suit": "clubs", "value": 10},]}, 
                            {"Joe": [{"name": "K", "suit": "hearts", "value": 13}, {"name": "K", "suit": "diamonds", "value": 13}]},
                            {"Eman": [{"name": "10", "suit": "hearts", "value": 10}, {"name": "A", "suit": "hearts", "value": 1}]},
                            ],
            "deck": [],
            "table_cards": [{"name": "2", "suit": "hearts", "value": 2}, {"name": "Q", "suit": "hearts", "value": 12},
                      {"name": "A", "suit": "diamonds", "value": 1}, {"name": "10", "suit": "spades", "value": 10},
                      {"name": "4", "suit": "hearts", "value": 4}],
            "last_card_dealt": 0,
            "player_order": ["Sergio", "Joe"],
            "current_turn": "Sergio",
            "turn_number": 0,
            "player_cards_dealt": False,
            "flop_dealt": False,
            "turn_dealt": False,
            "river_dealt": False
        }]  


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


hand_evaluations = [
        is_one_pair,
        is_two_pair,
        is_three_of_a_kind,
        is_straight,
        is_flush,
        # is_one_pair,
        # get_high_card,
    ]

hand_scores = {
     "is_one_pair": 20,
     "is_two_pair": 30,
     "is_three_of_a_kind": 40,
     "is_straight": 50,
     "is_flush": 60,
}


winners = {}


def evaluate_hand(player_cards, all_table_cards, player):
    print(f"evaluating hand...")
    # print(winners)
    all_cards = player_cards + all_table_cards
    [all_cards.append({"name": "A", "suit": card["suit"], "value": 14}) for card in all_cards if card["value"] == 1]
    all_combinations = list(combinations(all_cards, 5))
    player_card_values = [player_cards[0]["value"], player_cards[1]["value"]]
    max_score = 0
    players_in_winners = list(winners.keys())
    if len(players_in_winners) > 0:
        max_score = winners[players_in_winners[0]]["score"]
    # print(len(all_combinations))
    for evaluation in hand_evaluations:
        score = 0
        for combination in all_combinations:
            evaluation_result = evaluation(combination)
            if evaluation_result:
                score = hand_scores[evaluation.__name__]
                # print(f"This is the score: {score} this is the max {max_score}")
                if score > max_score:
                    # max_score = score
                    winners.clear()
                    winners[player] = {"name": player, "score": score, 
                                    "pair_value": evaluation_result, "hand_sum": sum(player_card_values)}
                elif score == max_score: 
                        winners[player] = {"name": player, "score": score, 
                                    "pair_value": evaluation_result, "hand_sum": sum(player_card_values)}
        
    #CHECK REAL WINNER NOW


                    
             
for player_dict in game_rooms[0]["player_list"]:
    player = list(player_dict.keys())[0]
    # number_of_players = len(game_rooms[0]["player_list"])
    evaluate_hand((player_dict[player]), game_rooms[0]["table_cards"], player)
# winner_player = max(list(winners.values()), key=lambda x: x['score'])
if len(list(winners.keys())) == 1:
     print("on first check")
     print(winners)
     print(list(winners.keys())[0])
else:
    filter_winners_list = {list(winners.keys())[0]: winners[list(winners.keys())[0]]}
    for player in winners:
        curr_player = winners[player]
        curr_name = curr_player["name"]
        winner_name = filter_winners_list[list(filter_winners_list.keys())[0]]["name"]
        if curr_player["pair_value"] > filter_winners_list[winner_name]["pair_value"] and curr_player["name"] != filter_winners_list[winner_name]["name"]:
             filter_winners_list.clear()
             filter_winners_list[curr_player["name"]] = curr_player
             print(filter_winners_list[curr_player["name"]])
        elif curr_player["pair_value"] == filter_winners_list[winner_name]["pair_value"] and curr_player["name"] != filter_winners_list[winner_name]["name"]:
            filter_winners_list[curr_player["name"]] = curr_player
    if len(list(filter_winners_list.keys())) == 1:
        print("We got a winner when comparing the value of the pairs in hand")
        print(list(filter_winners_list.keys()))
    else:
        print("Final Run through")
        final_winners = {list(filter_winners_list.keys())[0]: filter_winners_list[list(filter_winners_list.keys())[0]]}
        for player in filter_winners_list:
            curr_player = filter_winners_list[player]
            curr_name = curr_player["name"]
            winner_name = filter_winners_list[list(filter_winners_list.keys())[0]]["name"]
            if curr_player["hand_sum"] > final_winners[winner_name]["hand_sum"] and curr_player["name"] != final_winners[winner_name]["name"]:
                final_winners.clear()
                final_winners[curr_player["name"]] = curr_player
            elif curr_player["hand_sum"] == final_winners[winner_name]["hand_sum"] and curr_player["name"] != final_winners[winner_name]["name"]:
                final_winners[curr_player["name"]] = curr_player
        if len(list(final_winners.keys())) == 1:
            print("Final run has 1 winner indicated by hand sum")
            print(final_winners)
            print(list(final_winners.keys()))
        else:
            print("Multiple Winners")
            print(list(final_winners.keys()))

              
         
             
     


        