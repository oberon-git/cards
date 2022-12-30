import pygame
from .deck import Deck
from .player import Player
from .game_data import CARD_WIDTH
from .game_data import CARD_HEIGHT
from src.new.client.client_data import WIN_WIDTH
from src.new.client.client_data import WIN_HEIGHT

HAND_SIZE = 7


def outline_card(win, x, y, color=(255, 255, 0)):
    rect = (x - 2, y - 2, CARD_WIDTH + 2, CARD_HEIGHT + 2)
    pygame.draw.rect(win, color, rect, width=2)


def draw_center_lines(win):
    pygame.draw.line(win, (0, 0, 0), (0, WIN_HEIGHT // 2), (WIN_WIDTH, WIN_HEIGHT // 2))
    pygame.draw.line(win, (0, 0, 0), (WIN_WIDTH // 2, 0), (WIN_WIDTH // 2, WIN_HEIGHT))


def card_selected(x, y, pos):
    if x <= pos[0] <= x + CARD_WIDTH:
        if y <= pos[1] <= y + CARD_HEIGHT:
            return True
    return False


class Rummy:
    def __init__(self):
        self.deck = Deck()
        self.players = [Player(self.deck.deal_hand(HAND_SIZE)), Player(self.deck.deal_hand(HAND_SIZE))]
        self.top = self.deck.deal_card()
        self.bottom = None
        self.new_card_index = -1
        self.turn = 0
        self.step = 0
        self.winner = -1
        self.over = self.reset = self.update = self.show_opponents_hand = False
        self.back = "castle_back_01"

    def draw(self, win, resources, p, mouse_pos, clicked, frames):
        self.win.fill(pygame.color.Color())

        resources.draw_background(win, 1)
        self.back = "castle_back_0" + str(((frames // 32) % 2) + 1)
        if self.over:
            self.draw_winner(win, p)
            # self.play_again_button.draw(win, mouse_pos, clicked, resources)
        else:
            self.draw_pointer(win, resources, p)
        spacing = 20
        mult = CARD_WIDTH + spacing
        offset = (WIN_WIDTH - (len(self.players[p].hand()) * mult) + spacing) // 2
        hand = self.players[p].hand()
        to_discard = (False, -1, -1)
        for i in range(len(hand)):
            c = hand[i]
            x = i * mult + offset
            y = WIN_HEIGHT - CARD_HEIGHT - 30
            c.draw(win, resources, x, y)
            if self.turn == p and self.step == 1 and not self.over and card_selected(x, y, mouse_pos):
                outline_card(win, x, y)
                if clicked:
                    to_discard = (True, p, c)
            elif self.turn == p and self.step == 1 and not self.over and self.new_card_index == i:
                if (frames // 32) % 2 == 0:
                    outline_card(win, x, y, (0, 0, 0))
        if to_discard[0]:
            self.discard_card(to_discard[1], to_discard[2])

        if self.show_opponents_hand:
            o = 0 if p == 1 else 1
            hand = self.players[o].hand()
            for i in range(len(hand)):
                c = hand[i]
                x = i * mult + offset
                y = 30
                c.draw(win, resources, x, y)
        else:
            n = self.n + 1 if self.turn != p and self.step == 1 else self.n
            offset = (WIN_WIDTH - (n * mult) + spacing) // 2
            for i in range(n):
                resources.draw_card(win, self.back, i * mult + offset, 30)

        x = WIN_WIDTH // 2 - CARD_WIDTH // 2 - mult // 2
        y = WIN_HEIGHT // 2 - CARD_HEIGHT // 2
        resources.draw_card(win, self.back, x, y)
        if self.turn == p and self.step == 0 and not self.over and card_selected(x, y, mouse_pos):
            outline_card(win, x, y)
            if clicked:
                self.draw_card_from_deck(p)
        x += mult
        if self.over:
            resources.draw_card(win, self.back, x, y)
        elif self.top is not None:
            resources.draw_card(win, self.top.card(), x, y)
            if self.turn == p and self.step == 0 and card_selected(x, y, mouse_pos):
                outline_card(win, x, y)
                if clicked:
                    self.draw_top_card(p)

    def draw_pointer(self, win, resources, p):
        if p == self.turn:
            resources.draw_arrow(win, (WIN_WIDTH // 2 - 25 // 2, WIN_HEIGHT - 150 - 25), 0)
        else:
            resources.draw_arrow(win, (WIN_WIDTH // 2 - 25 // 2, 150), 1)

    def play_again(self):
        self.reset = True
        self.update = True

    def set_opponent(self, player, p):
        o = 0 if p == 1 else 1
        self.players[o] = player
        self.show_opponents_hand = True

    def get_player(self, p):
        return self.players[p]

    def set_player(self, player, p):
        self.players[p] = player

    def draw_winner(self, win, p):
        font = pygame.font.SysFont('Times', 30)
        if self.winner == p:
            text = font.render("You Won!", True, (255, 255, 255))
        else:
            text = font.render("You Lost!", True, (255, 255, 255))
        rect = text.get_rect()
        rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 100)
        win.blit(text, rect)

    def draw_card_from_deck(self, p):
        self.new_card_index = self.players[p].draw_card(self.deck.deal_card())
        self.step = 1
        self.update = True

    def draw_top_card(self, p):
        self.new_card_index = self.players[p].draw_card(self.top)
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

