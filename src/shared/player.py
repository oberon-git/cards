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

    def won(self):
        copy = self.h.copy()
        self.sort_by_suit()
        self.h.sort()
        runs = []
        c = 0
        while c < len(self.h):
            run = set()
            run.add(self.h[c])
            while c < len(self.h)-1 and self.h[c].suit() == self.h[c+1].suit() and (self.h[c].value() == self.h[c+1].value()-1 or self.h[c].value() == 13 and self.h[c+1].value() == 1):
                c += 1
                run.add(self.h[c])
                if c < len(self.h)-1 and self.h[c].value() == 13 and self.h[c+1].value() == 1:
                    break
            if len(run) >= 3:
                runs.append(run)
            c += 1

        self.sort_by_value()
        self.h.sort()
        pairs = []
        c = 0
        while c < len(self.h):
            pair = set()
            pair.add(self.h[c])
            while c < len(self.h)-1 and self.h[c].value() == self.h[c+1].value():
                c += 1
                pair.add(self.h[c])
            if len(pair) >= 3:
                pairs.append(pair)
            c += 1
        self.h = copy

        for i in range(len(runs)-1):
            if len(runs[i]) == 7:
                return True
            for j in range(i+1, len(runs)):
                if len(runs[i]) + len(runs[j]) == 7:
                    return True
        for i in range(len(pairs)-1):
            for j in range(i+1, len(pairs)):
                if len(pairs[i]) + len(pairs[j]) == 7:
                    return True
        for pair in pairs:
            for run in runs:
                points = len(run)
                for card in pair:
                    if card in run:
                        points -= 1
                if points + len(pair) == 7:
                    return True
        return False

    def sort_by_suit(self):
        for c in self.h:
            c.sort_by_suit()

    def sort_by_value(self):
        for c in self.h:
            c.sort_by_value()
