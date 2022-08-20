import pygame
import yaml
import _pickle as pickle
from random import shuffle

pygame.init()

with open("../appsettings.yml", 'r') as app_file:
    appsettings = yaml.safe_load(app_file)

WIN_WIDTH = appsettings["window"]["width"]
WIN_HEIGHT = appsettings["window"]["width"]
FPS = appsettings["window"]["width"]
BUTTON_WIDTH = appsettings["buttons"]["classic"]["width"]
BUTTON_HEIGHT = appsettings["buttons"]["classic"]["height"]
IMAGE_BUTTON_WIDTH = appsettings["buttons"]["images"]["width"]
IMAGE_BUTTON_HEIGHT = appsettings["buttons"]["images"]["height"]
GAMES = appsettings["games"]
BACKGROUND_COUNT = appsettings["backgrounds"]["count"]
CARD_TYPES = appsettings["cards"]["types"]
CARD_SUITS = appsettings["cards"]["suits"]
CARD_BACKS = appsettings["cards"]["backs"]
CARD_WIDTH = appsettings["cards"]["width"]
CARD_HEIGHT = appsettings["cards"]["height"]
CARD_SPACING = appsettings["cards"]["spacing"]
OUTLINE_WIDTH = 3
HOST = "173.230.150.237"
if appsettings["local"]:
    HOST = "localhost"
PORT = 13058
ADDR = (HOST, PORT)
END = str.encode("EOF")

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (100, 100, 100)
BUTTON = (200, 200, 200)
OUTLINE = (255, 255, 0)


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
        game = recv_packet(conn)
        while type(game) != Game:
            send_packet(conn, None)
            game = recv_packet(conn)
        return game
    except Exception as e:
        print(e)


def send_packet(conn, packet):
    conn.sendall(pickle.dumps(packet))


def recv_packet(conn):
    packet = pickle.loads(conn.recv(2048*4))
    if type(packet) == Packet:
        return packet
    if type(packet) == Deck:
        players = recv_packet(conn)
        if type(players) == list:
            return Game(packet, players)
        return players
    return packet


def card_selected(x, y, pos):
    if x <= pos[0] <= x + CARD_WIDTH:
        if y <= pos[1] <= y + CARD_HEIGHT:
            return True
    return False


def outline_card(win, x, y):
    rect = (x - OUTLINE_WIDTH, y - OUTLINE_WIDTH, CARD_WIDTH + OUTLINE_WIDTH, CARD_HEIGHT + OUTLINE_WIDTH)
    pygame.draw.rect(win, OUTLINE, rect, width=OUTLINE_WIDTH)


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
        self.n = 7
        if deck is None:
            self.deck = Deck()
        else:
            self.deck = deck
        if players is None:
            self.players = [Player(self.deck.deal_hand(self.n)), Player(self.deck.deal_hand(self.n))]
        else:
            self.players = players
        self.top = self.deck.deal_card()
        self.bottom = None
        self.turn = 0
        self.step = 0
        self.winner = -1
        self.over = self.reset = self.update = False
        self.back = "castle_back_01"
        self.play_again_button = Button((WIN_WIDTH // 2 - BUTTON_WIDTH // 2, WIN_HEIGHT // 2 + 100), "Play Again", self.play_again)

    def reshuffle(self):
        self.deck = Deck()
        self.players = [Player(self.deck.deal_hand(self.n)), Player(self.deck.deal_hand(self.n))]
        self.top = self.deck.deal_card()
        self.bottom = None
        self.turn = 0
        self.step = 0
        self.winner = -1
        self.over = self.reset = self.update = False

    def draw(self, win, resources, settings, p, mouse_pos, clicked, count):
        self.back = "castle_back_0" + str(((count // 8) % 2) + 1)
        resources.draw_background(win, settings.background)
        if self.winner > -1:
            self.draw_winner(win, p)
            self.play_again_button.draw(win, mouse_pos, clicked, resources)
        mult = CARD_WIDTH + CARD_SPACING
        offset = (WIN_WIDTH - (len(self.players[p].hand()) * mult) + CARD_SPACING) // 2
        hand = self.players[p].hand()
        to_discard = (False, -1, -1)
        for i in range(len(hand)):
            c = hand[i]
            x = i * mult + offset
            y = WIN_HEIGHT - CARD_HEIGHT - 30
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
        offset = (WIN_WIDTH - (n * mult) + CARD_SPACING) // 2
        for j in range(n):
            resources.draw_card(win, self.back, j * mult + offset, 30)

        x = WIN_WIDTH // 2 - CARD_WIDTH // 2 - mult // 2
        y = WIN_HEIGHT // 2 - CARD_HEIGHT // 2
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
        rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 100)
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
    def __init__(self, pos, content, action, selected=False):
        self.pos = pos
        self.action = action
        self.selected = selected
        if type(content) == str:
            self.type = 0
            self.rect = (pos[0], pos[1], BUTTON_WIDTH, BUTTON_HEIGHT)
            self.font = pygame.font.SysFont("Times", 30)
            self.text = self.font.render(content, False, BLACK)
            self.font_rect = self.text.get_rect()
            self.font_rect.center = (pos[0] + BUTTON_WIDTH // 2, pos[1] + BUTTON_HEIGHT // 2)
        if type(content) == int:
            self.type = 1
            self.rect = (pos[0], pos[1], IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT)
            self.key = content
        if content is None:
            self.type = 2
            self.rect = (self.pos[0], self.pos[1], 30, 40)

    def outline(self, win):
        if self.type != 2:
            rect = (self.rect[0] - OUTLINE_WIDTH, self.rect[1] - OUTLINE_WIDTH, self.rect[2] + OUTLINE_WIDTH, self.rect[3] + OUTLINE_WIDTH)
            pygame.draw.rect(win, OUTLINE, rect, width=OUTLINE_WIDTH)

    def in_range(self, pos):
        if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2]:
            if self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
                return True
        return False

    def click(self):
        if self.type == 1:
            self.action(self.key)
        else:
            self.action()

    def draw_button(self, win):
        pygame.draw.rect(win, BUTTON, self.rect)

    def draw_pause_button(self, win):
        pygame.draw.rect(win, BLACK, (self.pos[0], self.pos[1], 10, 40))
        pygame.draw.rect(win, BLACK, (self.pos[0] + 20, self.pos[1], 10, 40))

    def draw(self, win, mouse_pos, clicked, resources):
        if self.type == 0:
            self.draw_button(win)
            win.blit(self.text, self.font_rect)
        elif self.type == 1:
            resources.draw_background_select(win, self.key, self.pos)
        elif self.type == 2:
            self.draw_pause_button(win)
        if self.in_range(mouse_pos):
            self.outline(win)
            if clicked:
                self.click()
        elif self.selected:
            self.outline(win)
