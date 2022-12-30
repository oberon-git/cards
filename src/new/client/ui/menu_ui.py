import pygame
from .. import client_data
from .text_button import TextButton
from .text_button import TEXT_BUTTON_WIDTH


class MenuUI:
    def __init__(self, win, resources):
        self.win = win
        self.resources = resources
        self.start_game = False
        x_center = client_data.WIN_WIDTH // 2
        y_center = client_data.WIN_HEIGHT // 2
        self.play_button = TextButton(self.win, (x_center - TEXT_BUTTON_WIDTH // 2, y_center - 100),
                                      'Play', self.play_button_onclick)

    def draw(self, mouse_pos, clicked):
        pygame.draw.rect(self.win, pygame.color.Color(255, 255, 255),
                         (0, 0, client_data.WIN_WIDTH, client_data.WIN_HEIGHT))
        self.play_button.draw(mouse_pos, clicked)

    def play_button_onclick(self):
        self.start_game = True

