# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import UserDict, UserList
from datetime import timezone
from xml.dom import ValidationErr

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from random import shuffle

class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='members/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.nameme
    
    
# class Card(models.Model):
#     SUITS = (
#         ('H', 'Hearts'),
#         ('D', 'Diamonds'),
#         ('C', 'Clubs'),
#         ('S', 'Spades'),
#     )

#     RANKS = (
#         ('2', 'Two'),
#         ('3', 'Three'),
#         ('4', 'Four'),
#         ('5', 'Five'),
#         ('6', 'Six'),
#         ('7', 'Seven'),
#         ('8', 'Eight'),
#         ('9', 'Nine'),
#         ('10', 'Ten'),
#         ('J', 'Jack'),
#         ('Q', 'Queen'),
#         ('K', 'King'),
#         ('A', 'Ace'),
#     )

#     suit = models.CharField(max_length=1, choices=SUITS)
#     rank = models.CharField(max_length=2, choices=RANKS)
#     image = models.ImageField(upload_to='cards', null=True, blank=True)

#     def __str__(self):
#         return "{} of {}".format(self.rank, self.get_suit_display())

#class card for showing card rank and suit in the game image card with card rank and suit
SUITS = (
    ('H', 'Hearts'),
    ('D', 'Diamonds'),
    ('C', 'Clubs'),
    ('S', 'Spades'),
)

RANKS = (
    ('2', 'Two'),
    ('3', 'Three'),
    ('4', 'Four'),
    ('5', 'Five'),
    ('6', 'Six'),
    ('7', 'Seven'),
    ('8', 'Eight'),
    ('9', 'Nine'),
    ('10', 'Ten'),
    ('J', 'Jack'),
    ('Q', 'Queen'),
    ('K', 'King'),
    ('A', 'Ace'),
)

class Card:
    PROPERTIES = [(suit, rank) for suit, suit_name in SUITS for rank, rank_name in RANKS]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def get_value(self):
        if self.rank == 'A':
            return 11
        elif self.rank in ['J', 'Q', 'K']:
            return 10
        else:
            return int(self.rank)

    @property
    def full_name(self):
        return f"{dict(RANKS)[self.rank]} of {dict(SUITS)[self.suit]}"




class Blackjack:
    def __init__(self, players):
        self.deck = self.create_deck()
        self.players = players
        self.dealer_cards = []
        self.players_cards = [[] for _ in players]

    def create_deck(self):
        deck = [Card(suit, rank) for suit, rank in Card.RANKS * 4]
        shuffle(deck)
        return deck

    def deal_initial_cards(self):
        for i in range(2):
            for player_cards in self.players_cards:
                player_cards.append(self.deck.pop())
            self.dealer_cards.append(self.deck.pop())

    def is_blackjack(self, cards):
        if len(cards) != 2:
            return False
        ranks = [card.rank for card in cards]
        return ('A' in ranks and 'K' in ranks) or ('A' in ranks and 'Q' in ranks) or ('A' in ranks and 'J' in ranks) or ('K' in ranks and 'A' in ranks) or ('Q' in ranks and 'A' in ranks) or ('J' in ranks and 'A' in ranks) or sum(card.get_value() for card in cards) == 21

    def get_hand_value(self, cards):
        value = sum(card.get_value() for card in cards)
        num_aces = sum(1 for card in cards if card.rank == 'A')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    def play(self):
        self.deal_initial_cards()
        for i, player in enumerate(self.players):
            print(f"{player.name}'s turn:")
            while True:
                print(f"Your cards: {[str(card) for card in self.players_cards[i]]}")
                print(f"Dealer's card: {self.dealer_cards[0]}")
                choice = input("Do you want to hit or stand? ")
                if choice.lower() == 'hit':
                    self.players_cards[i].append(self.deck.pop())
                    value = self.get_hand_value(self.players_cards[i])
                    if value > 21:
                        print(f"Bust! Your hand value is {value}")
                        break
                else:
                    break
            print()
        dealer_value = self.get_hand_value(self.dealer_cards)
        while dealer_value < 17:
            self.dealer_cards.append(self.deck.pop())
            dealer_value = self.get_hand_value(self.dealer_cards)
        print(f"Dealer's cards: {[str(card) for card in self.dealer_cards]}")
        if dealer_value > 21:
            print("Dealer busts!")
            for i, player in enumerate(self.players):
                player_amount = player.amount
                player_hand_value = self.get_hand_value(self.players_cards[i])
                if self.is_blackjack(self.players_cards[i]):
                    player_amount *= 2.5
                else:
                    player_amount *= 2
                if player_hand_value > 21:
                    print(f"{player.name} busts! You lose {player.amount}")
                    player.amount -= player_amount
                elif self.is_blackjack(self.players_cards[i]):
                    print(f"Blackjack! {player.name} wins {player_amount}")
                    player.amount += player_amount
                elif self.get_hand_value(self.players_cards[i]) > dealer_value:
                    print(f"{player.name} wins {player_amount}")
                    player.amount += player_amount
                elif self.get_hand_value(self.players_cards[i]) == dealer_value:
                    print


def score(hand):
    """
    Calculate the score of a hand.

    A hand is a list of cards.
    """
    score = 0
    num_aces = 0

    for card in hand:
        if card.rank == 'A':
            num_aces += 1
        elif card.rank in ['K', 'Q', 'J']:
            score += 10
        else:
            score += int(card.rank)

    # Handle aces
    for i in range(num_aces):
        if score + 11 > 21:
            score += 1
        else:
            score += 11

    return score
