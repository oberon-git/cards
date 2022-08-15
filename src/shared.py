import pygame
import _pickle as pickle
from random import shuffle

LOCAL = False
# Data
CARD_TYPES = {1: "ace", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "jack", 12: "queen", 13: "king"}
CARD_SUITS = {1: "spades", 2: "hearts", 3: "clubs", 4: "diamonds"}
CARD_BACKS = ("castle_back_01", "castle_back_02")
CARD_WIDTH = 69
CARD_HEIGHT = 94
HOST = "173.230.150.237"
if LOCAL:
    HOST = "localhost"
PORT = 13058
ADDR = (HOST, PORT)
END = str.encode("EOF")
# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (100, 100, 100)
BUTTON = (200, 200, 200)


def send_str(conn, s):
    conn.sendall(str.encode(s))


def recv_str(conn):
    return conn.recv(512).decode()


def send_initial_game(conn, game):
    try:
        conn.sendall(pickle.dumps(game.deck))
        conn.sendall(pickle.dumps(game.players))
        return True
    except Exception as e:
        print(e)
        return False


def recv_initial_game(conn):
    try:
        deck = pickle.loads(conn.recv(2048*4))
        players = pickle.loads(conn.recv(2048*4))
        return Game(deck, players)
    except Exception as e:
        print(e)


def send_packet(conn, packet):
    conn.sendall(pickle.dumps(packet))


def recv_packet(conn):
    return pickle.loads(conn.recv(2048*2))


def card_selected(x, y, pos):
    if x <= pos[0] <= x + CARD_WIDTH:
        if y <= pos[1] <= y + CARD_HEIGHT:
            return True
    return False


def outline_card(win, x, y):
    pygame.draw.rect(win, (0, 0, 0), (x-2, y-2, CARD_WIDTH+2, CARD_HEIGHT+2), width=4)


def map_to_game(packet, game):
    game.turn = packet.turn
    game.step = packet.step
    game.top = packet.top
    game.bottom = packet.bottom
    game.deck.curr = packet.curr
    game.winner = packet.winner
    game.reset = packet.reset


class Packet:
    def __init__(self, game):
        self.turn = game.turn
        self.step = game.step
        self.top = game.top
        self.bottom = game.bottom
        self.curr = game.deck.curr
        self.winner = game.winner
        self.reset = game.reset
        self.connected = self.disconnected = False


class Game:
    def __init__(self, deck=None, players=None):
        pygame.init()
        self.n = 7
        if deck is None:
            self.deck = Deck()
        else:
            self.deck = deck
        if players is None:
            self.players = [Player(self.deck.deal_hand(self.n)), Player(self.deck.deal_hand(self.n))]
        else:
            self.players = players
        self.play_again_button = Button((750 // 2 - 100, 750 // 2 + 50, 200, 50), "Play Again", self.play_again)
        self.top = self.deck.deal_card()
        self.bottom = None
        self.back = "castle_back_01"
        self.turn = 0
        self.step = 0
        self.winner = -1
        self.over = self.reset = self.update = False

    def draw(self, win, resources, p, mouse_pos, clicked, count):
        self.back = "castle_back_0" + str(((count // 24) % 2) + 1)
        resources.draw_background(win, 2)
        if self.winner > -1:
            self.draw_winner(win, p)
            self.play_again_button.draw(win)
            if clicked:
                self.play_again_button.click(mouse_pos)
        mult = CARD_WIDTH + 20
        offset = (win.get_width() - (len(self.players[p].hand()) * mult) + 20) // 2
        hand = self.players[p].hand()
        to_discard = (False, -1, -1)
        for i in range(len(hand)):
            c = hand[i]
            x = i * mult + offset
            y = win.get_height() - CARD_HEIGHT - 30
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

        x = win.get_width() // 2 - CARD_WIDTH // 2 - mult // 2
        y = win.get_height() // 2 - CARD_HEIGHT // 2
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

    def play_again(self):
        self.reset = True
        self.update = True

    def draw_winner(self, win, p):
        font = pygame.font.SysFont("Times", 30)
        if self.winner == p:
            text = font.render("You Won!", True, WHITE)
        else:
            text = font.render("You Lost!", True, WHITE)
        rect = text.get_rect()
        rect.center = (win.get_width() // 2, win.get_height() // 2 - 100)
        win.blit(text, rect)

    def draw_card_from_deck(self, p):
        self.players[p].draw_card(self.deck.deal_card())
        self.step = 1
        self.update = True

    def draw_top_card(self, p):
        self.players[p].draw_card(self.top)
        self.top = self.bottom
        self.bottom = None
        self.step = 1
        self.update = True

    def discard_card(self, p, c):
        self.players[p].play_card(c)
        if self.players[p].won():
            self.winner = p
            self.over = True
        self.bottom = self.top
        self.top = c
        self.step = 0
        self.turn = 0 if self.turn == 1 else 1
        self.update = True


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


class Player:
    def __init__(self, hand):
        self.h = hand
        self.h.sort()

    def play_card(self, c):
        self.h.remove(c)

    def draw_card(self, c):
        self.h.append(c)
        self.h.sort()

    def hand(self):
        return self.h

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


class Card:
    def __init__(self, v, s):
        self.v = v
        self.s = s
        self.c = CARD_TYPES[self.v] + CARD_SUITS[self.s]
        self.sort = 0

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


class Button:
    def __init__(self, rect, text, action):
        self.rect = rect
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont("Times", 30)
        self.font_rect = pygame.Rect(rect)

    def click(self, pos):
        if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2]:
            if self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
                self.action()

    def draw(self, win):
        pygame.draw.rect(win, BUTTON, self.rect)
        text = self.font.render(self.text, False, BLACK)
        win.blit(text, self.font_rect)


class Resources:
    def __init__(self, file_list):
        self.cards = {}
        self.backgrounds = {}
        for filename in file_list:
            if "cards" in filename:
                key = filename.replace("assets/cards/", "").replace("_of_", "").replace(".png", "")
                self.cards[key] = pygame.image.load(filename)
            elif "backgrounds" in filename:
                key = int(filename.replace("assets/backgrounds/", "").replace(".png", ""))
                self.backgrounds[key] = pygame.image.load(filename)

    def draw_card(self, win, key, x, y):
        image = self.cards[key]
        win.blit(image, (x, y))

    def draw_background(self, win, key):
        image = pygame.transform.scale(self.backgrounds[key], (win.get_width(), win.get_height()))
        win.blit(image, (0, 0))
