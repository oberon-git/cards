from random import shuffle
from .shared_data import CARD_TYPES, CARD_SUITS
from .card import Card


class Deck:
    def __init__(self):
        self.deck = []
        for card in CARD_TYPES.keys():
            for suit in CARD_SUITS.keys():
                c = Card(card, suit)
                self.deck.append(c)
        shuffle(self.deck)

    def deal_hand(self, n, face_up=True):
        return [self.deal_card(face_up) for _ in range(n)]

    def deal_card(self, face_up=True):
        c = self.deck.pop(0)
        c.face_up = face_up
        return c

    def is_empty(self):
        return len(self.deck) == 0
