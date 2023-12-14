#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Card

def create_cards():
    number_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    face_cards = ['J', 'Q', 'K', 'A']
    names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    cards = []
    value = 0

    for number in range(13):
        if names[number] in number_cards:
            value = int(names[number])
        elif names[number] == "A":
            value = 1
        elif names[number] == "J":
            value = 11
        elif names[number] == "Q":
            value = 12
        elif names[number] == "K":
            value = 13
        card1 = Card(name = names[number], suit = suits[0], value = value)
        card2 = Card(name = names[number], suit = suits[1], value = value)
        card3 = Card(name = names[number], suit = suits[2], value = value)
        card4 = Card(name = names[number], suit = suits[3], value = value)
        cards.append(card1)
        cards.append(card2)
        cards.append(card3)
        cards.append(card4)
    
    return cards
    
    

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
        print("clearing db...")
        Card.query.delete()
        db.session.commit()

        print("seeding cards...")
        all_cards = create_cards()
        db.session.add_all(all_cards)
        db.session.commit()
