class Player:
    def __init__(self, hand, sort_hand=False):
        self.h = hand
        self.sort_hand = sort_hand
        if self.sort_hand:
            self.h.sort()

    def play_card(self, card):
        i_to_pop = -1
        for i in range(len(self.h)):
            if self.h[i] == card:
                i_to_pop = i
                break
        if i_to_pop == -1:
            raise Exception('Card was not in hand.')
        return self.h.pop(i_to_pop)

    def replace_card(self, card_to_replace, new_card):
        i_to_replace = -1
        for i in range(len(self.h)):
            if self.h[i] == card_to_replace:
                i_to_replace = i
                break
        if i_to_replace == -1:
            raise Exception('Card was not in hand.')
        self.h[i_to_replace] = new_card


    def draw_card(self, c):
        self.h.append(c)
        if self.sort_hand:
            self.h.sort()
        return self.h.index(c)

    def flip(self, c):
        for card in self.h:
            if card == c:
                card.flip()
                break

    def hand(self):
        return self.h

    def set_hand(self, hand):
        self.h = hand

    def sort_by_suit(self):
        for c in self.h:
            c.sort_by_suit()
        self.h.sort()

    def sort_by_value(self):
        for c in self.h:
            c.sort_by_value()
        self.h.sort()
