import pygame
from .shared_data import CARD_WIDTH, CARD_HEIGHT, CENTER, BLINK_SPEED, CARD_SPACING, WIN_WIDTH, WIN_HEIGHT
from .shared_data import BLACK, WHITE, FONT_SIZE, FONT_FAMILY, ARROW_SIZE
from .game import Game, card_selected, outline_card


class Golf(Game):
    def __init__(self):
        super().__init__(6)

    def draw(self, win, resources, settings, p, mouse_pos, clicked, count, network):
        super().draw(win, resources, settings, p, mouse_pos, clicked, count, network)
