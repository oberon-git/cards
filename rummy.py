import pygame
from player import Player
from data import Data
from deck import Deck


def card_selected(x, y, pos):
    if x <= pos[0] <= x + Data.CARD_WIDTH:
        if y <= pos[1] <= y + Data.CARD_HEIGHT:
            return True
    return False


def outline_card(win, x, y):
    pygame.draw.rect(win, (0, 0, 0), (x-2, y-2, Data.CARD_WIDTH+2, Data.CARD_HEIGHT+2), width=4)


def find_max_run(hand, cards_used):
    max_run = 0
    for c in range(len(hand)):
        if hand[c].card() in cards_used:
            continue
        run = 1
        cards = set()
        while c < len(hand)-1 and hand[c].suit() == hand[c+1].suit() and (hand[c].value() == hand[c+1].value() - 1) or (hand[c].value() == 13 and hand[c+1].value() == 1):
            c += 1
            if hand[c].card() in cards_used:
                continue
            run += 1
            cards.add(hand[c].card())
            if hand[c].value() == 13 and hand[c+1].value() == 1:
                break
        if max_run < run:
            max_run = run
            for card in cards:
                cards_used.add(card)
    return max_run, cards_used


def find_max_pair(hand, cards_used):
    max_pair = 0
    for c in range(len(hand)):
        if hand[c].card() in cards_used:
            continue
        pair = 1
        cards = set()
        while c < len(hand)-1 and hand[c].value() == hand[c+1].value():
            c += 1
            if hand[c].card() in cards_used:
                continue
            pair += 1
            cards.add(hand[c].card())
        if pair > max_pair:
            max_pair = pair
            for card in cards:
                cards_used.add(card)
    return max_pair, cards_used


def won(hand):
    max_run, cards_used = find_max_run(hand, set())
    if max_run == 7:
        return True
    max_pair, cards_used = find_max_pair(hand, cards_used)
    if max_run + max_pair == 7 and max_run > 3 and max_pair > 3:
        return True
    max_pair, cards_used = find_max_pair(hand, set())
    max_run, cards_used = find_max_run(hand, cards_used)
    if max_run + max_pair == 7 and max_run > 3 and max_pair > 3:
        return True
    max_run, cards_used = find_max_run(hand, set())
    max_run += find_max_run(hand, cards_used)[0]
    if max_run == 7:
        return True
    max_pair, cards_used = find_max_pair(hand, set())
    max_pair += find_max_pair(hand, cards_used)[0]
    if max_pair == 7:
        return True
    return False


class Rummy:
    def __init__(self):
        self.n = 7
        self.deck = Deck()
        self.players = [Player(self.deck.deal_hand(self.n)), Player(self.deck.deal_hand(self.n))]
        self.top = self.deck.deal_card()
        self.bottom = None
        self.back = "castle_back_01"
        self.turn = 0
        self.step = 0
        self.winner = -1

    def draw(self, win, resources, p, mouse_pos, clicked):
        resources.draw_background(win, 7)
        if self.winner > -1:
            print(self.winner)
            self.draw_winner(win, p)
        mult = Data.CARD_WIDTH + 20
        offset = win.get_width() // 2 - mult * self.n // 2
        hand = self.players[p].hand()
        to_discard = (False, -1, -1)
        for i in range(len(hand)):
            c = hand[i]
            x = i * mult + offset
            y = win.get_height() - Data.CARD_HEIGHT - 30
            c.draw(win, resources, x, y)
            if self.turn == p and self.step == 1 and self.winner == -1 and card_selected(x, y, mouse_pos):
                outline_card(win, x, y)
                if clicked:
                    to_discard = (True, p, c)
        if to_discard[0]:
            self.discard_card(to_discard[1], to_discard[2])

        n = self.n
        if self.turn != p and self.step == 1:
            n += 1
            offset = win.get_width() // 2 - mult * 4
        for j in range(n):
            resources.draw_card(win, self.back, j * mult + offset, 30)

        x = win.get_width() // 2 - Data.CARD_WIDTH // 2 - mult // 2
        y = win.get_height() // 2 - Data.CARD_HEIGHT // 2
        resources.draw_card(win, self.back, x, y)
        if self.turn == p and self.step == 0 and self.winner == -1 and card_selected(x, y, mouse_pos):
            outline_card(win, x, y)
            if clicked:
                self.draw_card_from_deck(p)
        x += mult
        if self.top is not None:
            if self.winner > 0:
                resources.draw_card(win, self.back, x, y)
            else:
                resources.draw_card(win, self.top.card(), x, y)
        if self.turn == p and self.step == 0 and self.winner == -1 and card_selected(x, y, mouse_pos):
            outline_card(win, x, y)
            if clicked:
                self.draw_top_card(p)

    def draw_winner(self, win, p):
        font = pygame.font.SysFont(None, 30)
        if self.winner == p:
            text = font.render("You Won!", True, (255, 255, 255))
        else:
            text = font.render("You Lost!", True, (255, 255, 255))
        rect = text.get_rect()
        rect.center = (win.get_width() // 2, win.get_height() // 2 - 100)
        win.blit(text, rect)

    def draw_card_from_deck(self, p):
        self.players[p].draw_card(self.deck.deal_card())
        self.step = 1

    def draw_top_card(self, p):
        self.players[p].draw_card(self.top)
        self.top = self.bottom
        self.bottom = None
        self.step = 1

    def discard_card(self, p, c):
        self.players[p].play_card(c)
        if self.players[p].won():
            self.winner = p
        self.bottom = self.top
        self.top = c
        self.step = 0
        self.turn = 0 if p == 1 else 1
