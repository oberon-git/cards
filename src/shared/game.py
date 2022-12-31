import pygame
from .shared_data import CARD_WIDTH, CARD_HEIGHT, OUTLINE, OUTLINE_WIDTH, CENTER, BUTTON_WIDTH
from .shared_data import WIN_HEIGHT, FONT_FAMILY, FONT_SIZE, ARROW_SIZE, WHITE
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


class Game:
    def __init__(self, hand_size):
        self.hand_size = hand_size
        self.deck = Deck()
        self.players = [Player(self.deck.deal_hand(self.hand_size)), Player(self.deck.deal_hand(self.hand_size))]
        self.turn = 0
        self.winner = -1
        self.over = self.reset = False
        self.play_again_button = Button((CENTER[0] - BUTTON_WIDTH // 2, CENTER[1] + 100), "Play Again", self.play_again)

    def draw(self, win, resources, settings, p, mouse_pos, clicked, count, network):
        resources.draw_background(win, settings.background)

        if self.over:
            self.draw_winner(win, p)
            self.play_again_button.draw(win, mouse_pos, clicked, resources)
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
        else:
            text = font.render("You Lost!", True, WHITE)
        rect = text.get_rect()
        rect.center = (CENTER[0], CENTER[1] - 100)
        win.blit(text, rect)

    def play_again(self):
        self.reset = True
