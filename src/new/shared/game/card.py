from .game_data import CARD_TYPES
from .game_data import CARD_SUITS


class Card:
    def __init__(self, v, s):
        self.v = v
        self.s = s
        self.c = CARD_TYPES[self.v] + CARD_SUITS[self.s]
        self.sort = 1

    def draw(self, win, resources, x, y):
        resources.draw_card(win, self.c, x, y)

    def card(self):
        return self.c

    def value(self):
        return self.v

    def suit(self):
        return self.s

    def sort_by_suit(self):
        self.sort = 0

    def sort_by_value(self):
        self.sort = 1

    def __lt__(self, other):
        if self.sort == 0:
            if self.s == other.s:
                return self.v < other.v
            else:
                return self.s < other.s
        else:
            if self.v == other.v:
                return self.s < other.s
            else:
                return self.v < other.v

    def __gt__(self, other):
        if self.sort == 0:
            if self.s == other.s:
                return self.v > other.v
            else:
                return self.s > other.s
        else:
            if self.v == other.v:
                return self.s > other.s
            else:
                return self.v > other.v

    def __eq__(self, other):
        return self.s == other.s and self.c == other.c

    def __str__(self):
        return self.c

    def __hash__(self):
        return self.c.__hash__()
