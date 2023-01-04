import pygame
from .shared_data import CARD_WIDTH, CARD_HEIGHT, OUTLINE, OUTLINE_WIDTH, CENTER, BUTTON_WIDTH
from .shared_data import WIN_HEIGHT, FONT_FAMILY, FONT_SIZE, ARROW_SIZE, WHITE
from .deck import Deck
from .player import Player


def card_selected(x, y, pos):
    if x <= pos[0] <= x + CARD_WIDTH:
        if y <= pos[1] <= y + CARD_HEIGHT:
            return True
    return False


def outline_card(win, x, y, color=OUTLINE):
    rect = (x - OUTLINE_WIDTH, y - OUTLINE_WIDTH, CARD_WIDTH + OUTLINE_WIDTH + 2, CARD_HEIGHT + OUTLINE_WIDTH + 2)
    pygame.draw.rect(win, color, rect, width=OUTLINE_WIDTH)


class Game:
    def __init__(self, hand_size, sort_hand=False):
        self.hand_size = hand_size
        self.deck = Deck()
        self.players = [
            Player(self.deck.deal_hand(self.hand_size, False), sort_hand=sort_hand),
            Player(self.deck.deal_hand(self.hand_size, False), sort_hand=sort_hand)
        ]
        self.turn = 0
        self.winner = -1
        self.over = False

    def draw(self, win, resources, client_data, p, event, frame_count, network):
        resources.draw_background(win, client_data.settings.background)

        if self.over:
            self.draw_winner(win, p)
        else:
            self.draw_pointer(win, resources, p)

    def draw_pointer(self, win, resources, p):
        if p == self.turn:
            resources.draw_arrow(win, (CENTER[0] - ARROW_SIZE // 2, WIN_HEIGHT - 150 - ARROW_SIZE), 0)
        else:
            resources.draw_arrow(win, (CENTER[0] - ARROW_SIZE // 2, 150), 1)

    def draw_winner(self, win, p):
        font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
        if self.winner == p:
            text = font.render("You Won!", True, WHITE)
        elif self.winner == 1 - p:
            text = font.render("You Lost!", True, WHITE)
        else:
            text = font.render("It's a Tie!", True, WHITE)
        rect = text.get_rect()
        rect.center = (CENTER[0], CENTER[1] - 100)
        win.blit(text, rect)
