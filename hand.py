class Hand:
    def __init__(self, hand):
        self.h = hand
        self.sort()

    def remove_card(self, c):
        self.h.remove(c)

    def add_card(self, c):
        self.h.append(c)
        self.sort()

    def hand(self):
        return self.h

    def is_winning_hand(self):
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
                if self.h[c].value() == 13 and self.h[c+1].value() == 1:
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

        if len(runs) == 1:
            return True
        for i in range(len(runs)-1):
            for j in range(i+1, len(runs)):
                if len(runs[i]) + len(runs[j]) == 7:
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

    def sort(self):
        self.h.sort()

