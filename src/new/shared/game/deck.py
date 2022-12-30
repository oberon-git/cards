from random import shuffle
from .game_data import CARD_TYPES
from .game_data import CARD_SUITS
from .card import Card


class Deck:
    def __init__(self):
        self.deck = []
        for card in CARD_TYPES.keys():
            for suit in CARD_SUITS.keys():
                c = Card(card, suit)
                self.deck.append(c)
        shuffle(self.deck)
        self.curr = 0

    def get_deck(self):
        return self.deck

    def deal_hand(self, n):
        hand = []
        for _ in range(n):
            hand.append(self.deal_card())
        return hand

    def deal_card(self):
        c = self.deck[self.curr]
        self.curr += 1
        return c
