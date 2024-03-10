#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Card, User

def create_cards():

    cards = []

    # Spades
    card1 = Card(name = "A", suit = "Spades", value = 1, image = "https://deckofcardsapi.com/static/img/AS.png")
    cards.append(card1)
    card2 = Card(name = "2", suit = "Spades", value = 2, image = "https://deckofcardsapi.com/static/img/2S.png")
    cards.append(card2)
    card3 = Card(name = "3", suit = "Spades", value = 3, image = "https://deckofcardsapi.com/static/img/3S.png")
    cards.append(card3)
    card4 = Card(name = "4", suit = "Spades", value = 4, image = "https://deckofcardsapi.com/static/img/4S.png")
    cards.append(card4)
    card5 = Card(name = "5", suit = "Spades", value = 5, image = "https://deckofcardsapi.com/static/img/5S.png")
    cards.append(card5)
    card6 = Card(name = "6", suit = "Spades", value = 6, image = "https://deckofcardsapi.com/static/img/6S.png")
    cards.append(card6)
    card7 = Card(name = "7", suit = "Spades", value = 7, image = "https://deckofcardsapi.com/static/img/7S.png")
    cards.append(card7)
    card8 = Card(name = "8", suit = "Spades", value = 8, image = "https://deckofcardsapi.com/static/img/8S.png")
    cards.append(card8)
    card9 = Card(name = "9", suit = "Spades", value = 9, image = "https://deckofcardsapi.com/static/img/9S.png")
    cards.append(card9)
    card10 = Card(name = "10", suit = "Spades", value = 10, image = "https://deckofcardsapi.com/static/img/0S.png")
    cards.append(card10)
    card11 = Card(name = "J", suit = "Spades", value = 11, image = "https://deckofcardsapi.com/static/img/JS.png")
    cards.append(card11)
    card12 = Card(name = "Q", suit = "Spades", value = 12, image = "https://deckofcardsapi.com/static/img/QS.png")
    cards.append(card12)
    card13 = Card(name = "K", suit = "Spades", value = 13, image = "https://deckofcardsapi.com/static/img/KS.png")
    cards.append(card12)

    # Hearts
    card14 = Card(name = "A", suit = "Hearts", value = 1, image = "https://deckofcardsapi.com/static/img/AH.png")
    cards.append(card14)
    card15 = Card(name = "2", suit = "Hearts", value = 2, image = "https://deckofcardsapi.com/static/img/2H.png")
    cards.append(card15)
    card16 = Card(name = "3", suit = "Hearts", value = 3, image = "https://deckofcardsapi.com/static/img/3H.png")
    cards.append(card16)
    card17 = Card(name = "4", suit = "Hearts", value = 4, image = "https://deckofcardsapi.com/static/img/4H.png")
    cards.append(card17)
    card18 = Card(name = "5", suit = "Hearts", value = 5, image = "https://deckofcardsapi.com/static/img/5H.png")
    cards.append(card18)
    card19 = Card(name = "6", suit = "Hearts", value = 6, image = "https://deckofcardsapi.com/static/img/6H.png")
    cards.append(card19)
    card20 = Card(name = "7", suit = "Hearts", value = 7, image = "https://deckofcardsapi.com/static/img/7H.png")
    cards.append(card20)
    card21 = Card(name = "8", suit = "Hearts", value = 8, image = "https://deckofcardsapi.com/static/img/8H.png")
    cards.append(card21)
    card22 = Card(name = "9", suit = "Hearts", value = 9, image = "https://deckofcardsapi.com/static/img/9H.png")
    cards.append(card22)
    card23 = Card(name = "10", suit = "Hearts", value = 10, image = "https://deckofcardsapi.com/static/img/0H.png")
    cards.append(card23)
    card24 = Card(name = "J", suit = "Hearts", value = 11, image = "https://deckofcardsapi.com/static/img/JH.png")
    cards.append(card24)
    card25 = Card(name = "Q", suit = "Hearts", value = 12, image = "https://deckofcardsapi.com/static/img/QH.png")
    cards.append(card25)
    card26 = Card(name = "K", suit = "Hearts", value = 13, image = "https://deckofcardsapi.com/static/img/KH.png")
    cards.append(card26)
    # Clubs
    card27 = Card(name = "A", suit = "Clubs", value = 1, image = "https://deckofcardsapi.com/static/img/AC.png")
    cards.append(card27)
    card28 = Card(name = "2", suit = "Clubs", value = 2, image = "https://deckofcardsapi.com/static/img/2C.png")
    cards.append(card28)
    card29 = Card(name = "3", suit = "Clubs", value = 3, image = "https://deckofcardsapi.com/static/img/3C.png")
    cards.append(card29)
    card30 = Card(name = "4", suit = "Clubs", value = 4, image = "https://deckofcardsapi.com/static/img/4C.png")
    cards.append(card30)
    card31 = Card(name = "5", suit = "Clubs", value = 5, image = "https://deckofcardsapi.com/static/img/5C.png")
    cards.append(card31)
    card32 = Card(name = "6", suit = "Clubs", value = 6, image = "https://deckofcardsapi.com/static/img/6C.png")
    cards.append(card32)
    card33 = Card(name = "7", suit = "Clubs", value = 7, image = "https://deckofcardsapi.com/static/img/7C.png")
    cards.append(card33)
    card34 = Card(name = "8", suit = "Clubs", value = 8, image = "https://deckofcardsapi.com/static/img/8C.png")
    cards.append(card34)
    card35 = Card(name = "9", suit = "Clubs", value = 9, image = "https://deckofcardsapi.com/static/img/9C.png")
    cards.append(card35)
    card36 = Card(name = "10", suit = "Clubs", value = 10, image = "https://deckofcardsapi.com/static/img/0C.png")
    cards.append(card36)
    card37 = Card(name = "J", suit = "Clubs", value = 11, image = "https://deckofcardsapi.com/static/img/JC.png")
    cards.append(card37)
    card38 = Card(name = "Q", suit = "Clubs", value = 12, image = "https://deckofcardsapi.com/static/img/QC.png")
    cards.append(card38)
    card39 = Card(name = "K", suit = "Clubs", value = 13, image = "https://deckofcardsapi.com/static/img/KC.png")
    cards.append(card39)
    # Diamond

    card40 = Card(name = "A", suit = "Diamonds", value = 1, image = "https://deckofcardsapi.com/static/img/AD.png")
    cards.append(card40)
    card41 = Card(name = "2", suit = "Diamonds", value = 2, image = "https://deckofcardsapi.com/static/img/2D.png")
    cards.append(card41)
    card42 = Card(name = "3", suit = "Diamonds", value = 3, image = "https://deckofcardsapi.com/static/img/3D.png")
    cards.append(card42)
    card43 = Card(name = "4", suit = "Diamonds", value = 4, image = "https://deckofcardsapi.com/static/img/4D.png")
    cards.append(card43)
    card44 = Card(name = "5", suit = "Diamonds", value = 5, image = "https://deckofcardsapi.com/static/img/5D.png")
    cards.append(card44)
    card45 = Card(name = "6", suit = "Diamonds", value = 6, image = "https://deckofcardsapi.com/static/img/6D.png")
    cards.append(card45)
    card46 = Card(name = "7", suit = "Diamonds", value = 7, image = "https://deckofcardsapi.com/static/img/7D.png")
    cards.append(card46)
    card47 = Card(name = "8", suit = "Diamonds", value = 8, image = "https://deckofcardsapi.com/static/img/8D.png")
    cards.append(card47)
    card48 = Card(name = "9", suit = "Diamonds", value = 9, image = "https://deckofcardsapi.com/static/img/9D.png")
    cards.append(card48)
    card49 = Card(name = "10", suit = "Diamonds", value = 10, image = "https://deckofcardsapi.com/static/img/0D.png")
    cards.append(card49)
    card50 = Card(name = "J", suit = "Diamonds", value = 11, image = "https://deckofcardsapi.com/static/img/JD.png")
    cards.append(card50)
    card51 = Card(name = "Q", suit = "Diamonds", value = 12, image = "https://deckofcardsapi.com/static/img/QD.png")
    cards.append(card51)
    card52 = Card(name = "K", suit = "Diamonds", value = 13, image = "https://deckofcardsapi.com/static/img/KD.png")
    cards.append(card52)

    return cards
    
    # number_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    # face_cards = ['J', 'Q', 'K', 'A']
    # names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    # suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    # cards = []
    # value = 0

    # for number in range(13):
    #     if names[number] in number_cards:
    #         value = int(names[number])
    #     elif names[number] == "A":
    #         value = 1
    #     elif names[number] == "J":
    #         value = 11
    #     elif names[number] == "Q":
    #         value = 12
    #     elif names[number] == "K":
    #         value = 13
    #     card1 = Card(name = names[number], suit = suits[0], value = value)
    #     card2 = Card(name = names[number], suit = suits[1], value = value)
    #     card3 = Card(name = names[number], suit = suits[2], value = value)
    #     card4 = Card(name = names[number], suit = suits[3], value = value)
    #     cards.append(card1)
    #     cards.append(card2)
    #     cards.append(card3)
    #     cards.append(card4)
    
    # return cards
    
    

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
        print("clearing db...")
        Card.query.delete()
        db.session.commit()
        User.query.delete()
        db.session.commit()

        print("seeding cards...")
        all_cards = create_cards()
        db.session.add_all(all_cards)
        db.session.commit()
