import pygame
from src.shared.shared_data import *


class Resources:
    def __init__(self):
        self.cards = {}
        # self.card_backs = {}
        self.backgrounds = {}
        self.ui = {}

        for filename in os.listdir(f'{ASSET_DIR}/cards'):
            path = f'{ASSET_DIR}/cards/{filename}'
            key = filename.replace('cards/', '').replace('_of_', '').replace('.png', '')
            self.cards[key] = pygame.image.load(path)

        for filename in os.listdir(f'{ASSET_DIR}/card_backs'):
            path = f'{ASSET_DIR}/card_backs/{filename}'
            key = filename.replace('.png', '')
            self.cards[key] = pygame.image.load(path)

        for filename in os.listdir(f'{ASSET_DIR}/backgrounds'):
            path = f'{ASSET_DIR}/backgrounds/{filename}'
            key = int(filename.replace('backgrounds/', '').replace('.png', ''))
            self.backgrounds[key] = pygame.image.load(path)

        for filename in os.listdir(f'{ASSET_DIR}/ui'):
            path = f'{ASSET_DIR}/ui/{filename}'
            key = filename.replace('.png', '')
            self.ui[key] = pygame.image.load(path)

        self.icon = self.ui['icon']
        self.arrow = pygame.transform.rotate(pygame.transform.scale(self.ui['arrow'], (25, 25)), 180)

    def draw_card(self, win, key, x, y):
        image = self.cards[key]
        win.blit(image, (x, y))

    def draw_background(self, win, key):
        image = pygame.transform.scale(self.backgrounds[key], (WIN_WIDTH, WIN_HEIGHT))
        win.blit(image, (0, 0))

    def draw_background_select(self, win, key, pos):
        image = pygame.transform.scale(self.backgrounds[key], (100, 100))
        win.blit(image, pos)

    def draw_arrow(self, win, pos, orientation):
        image = pygame.transform.rotate(self.arrow, 180 if orientation == 0 else 0)
        win.blit(image, pos)
