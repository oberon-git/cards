import pygame
from .shared_data import *
from .commands import *
from .deck import Deck
from .player import Player
from .button import Button


def card_selected(x, y, pos):
    if x <= pos[0] <= x + CARD_WIDTH:
        if y <= pos[1] <= y + CARD_HEIGHT:
            return True
    return False


def outline_card(win, x, y, color=OUTLINE):
    rect = (x - OUTLINE_WIDTH, y - OUTLINE_WIDTH, CARD_WIDTH + OUTLINE_WIDTH, CARD_HEIGHT + OUTLINE_WIDTH)
    pygame.draw.rect(win, color, rect, width=OUTLINE_WIDTH)


class Rummy:
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
        self.new_card_index = -1
        self.turn = 0
        self.step = 0
        self.winner = -1
        self.over = self.reset = self.update = self.show_opponents_hand = False
        self.back = "castle_back_01"
        self.play_again_button = Button((CENTER[0] - BUTTON_WIDTH // 2, CENTER[1] + 100), "Play Again", self.play_again)

    def reshuffle(self):
        self.deck = Deck()
        self.players = [Player(self.deck.deal_hand(self.n)), Player(self.deck.deal_hand(self.n))]
        self.top = self.deck.deal_card()
        self.bottom = None
        self.turn = 0
        self.step = 0
        self.winner = -1
        self.over = self.reset = self.update = self.show_opponents_hand = False

    def draw(self, win, resources, settings, p, mouse_pos, clicked, count, network):
        resources.draw_background(win, settings.background)
        self.back = "castle_back_0" + str(((count // BLINK_SPEED) % 2) + 1)
        if self.over:
            self.draw_winner(win, p)
            self.play_again_button.draw(win, mouse_pos, clicked, resources)
        else:
            self.draw_pointer(win, resources, p)
        mult = CARD_WIDTH + CARD_SPACING
        offset = (WIN_WIDTH - (len(self.players[p].hand()) * mult) + CARD_SPACING) // 2
        hand = self.players[p].hand()

        for i in range(len(hand)):
            c = hand[i]
            x = i * mult + offset
            y = WIN_HEIGHT - CARD_HEIGHT - 30
            c.draw(win, resources, x, y)
            if self.turn == p and self.step == 1 and not self.over and card_selected(x, y, mouse_pos):
                outline_card(win, x, y)
                if clicked:  # send discard command
                    network.send_command_to_server(DiscardCommand(p, c))
            elif self.turn == p and self.step == 1 and not self.over and self.new_card_index == i:
                if (count // BLINK_SPEED) % 2 == 0:
                    outline_card(win, x, y, BLACK)

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
            offset = (WIN_WIDTH - (n * mult) + CARD_SPACING) // 2
            for i in range(n):
                resources.draw_card(win, self.back, i * mult + offset, 30)

        x = CENTER[0] - CARD_WIDTH // 2 - mult // 2
        y = CENTER[1] - CARD_HEIGHT // 2
        resources.draw_card(win, self.back, x, y)
        if self.turn == p and self.step == 0 and not self.over and card_selected(x, y, mouse_pos):
            outline_card(win, x, y)
            if clicked:
                network.send_command_to_server(DrawFromDeckCommand(p))
        x += mult
        if self.over:
            resources.draw_card(win, self.back, x, y)
        elif self.top is not None:
            resources.draw_card(win, self.top.card(), x, y)
            if self.turn == p and self.step == 0 and card_selected(x, y, mouse_pos):
                outline_card(win, x, y)
                if clicked:
                    network.send_command_to_server(DrawFromDiscardCommand(p))

    def draw_pointer(self, win, resources, p):
        if p == self.turn:
            resources.draw_arrow(win, (CENTER[0] - ARROW_SIZE // 2, WIN_HEIGHT - 150 - ARROW_SIZE), 0)
        else:
            resources.draw_arrow(win, (CENTER[0] - ARROW_SIZE // 2, 150), 1)

    def play_again(self):
        self.reset = True

    def set_opponent(self, player, p):
        o = 1 - p
        self.players[o] = player
        self.show_opponents_hand = True

    def get_player(self, p):
        return self.players[p]

    def set_player(self, player, p):
        self.players[p] = player

    def draw_winner(self, win, p):
        font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
        if self.winner == p:
            text = font.render("You Won!", True, WHITE)
        else:
            text = font.render("You Lost!", True, WHITE)
        rect = text.get_rect()
        rect.center = (CENTER[0], CENTER[1] - 100)
        win.blit(text, rect)

    def draw_card_from_deck(self, p):
        self.new_card_index = self.players[p].draw_card(self.deck.deal_card())
        self.step = 1

    def draw_top_card(self, p):
        self.new_card_index = self.players[p].draw_card(self.top)
        self.top = self.bottom
        self.bottom = None
        self.step = 1

    def discard_card(self, p, c):
        self.players[p].play_card(c)
        if self.players[p].won():
            self.winner = p
            self.over = True
        self.bottom = self.top
        self.top = c
        self.step = 0
        self.turn = 1 - self.turn
