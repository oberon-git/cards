from hand import Hand


class Player:
    def __init__(self, hand):
        self.h = Hand(hand)
        self.hand.sort()

    def hand(self):
        return self.h.hand()

    def play_card(self, c):
        self.h.add_card(c)

    def draw_card(self, c):
        self.h.remove_card(c)
