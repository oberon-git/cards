import pygame
import os
from src.shared.shared_data import ASSET_DIR, WIN_WIDTH, WIN_HEIGHT, CARD_BACKS


class Resources:
    def __init__(self):
        self.cards = {}
        self.card_overlays = {}
        self.card_backs = {}
        self.card_back_overlays = {}
        self.backgrounds = {}
        self.ui = {}

        for filename in os.listdir(f'{ASSET_DIR}/cards'):
            path = f'{ASSET_DIR}/cards/{filename}'
            key = filename.replace('_of_', '').replace('.png', '')
            self.cards[key] = pygame.image.load(path)

        for filename in os.listdir(f'{ASSET_DIR}/card_overlays'):
            path = f'{ASSET_DIR}/card_overlays/{filename}'
            key = filename.replace('_of_', '').replace('.png', '')
            self.card_overlays[key] = pygame.image.load(path)

        for key, data in CARD_BACKS.items():
            if data['frames'] == 1:
                path = f'{ASSET_DIR}/card_backs/{key}.png'
                self.card_backs[key] = CardBack([pygame.image.load(path)])
            else:
                frames = []
                for i in range(1, data['frames'] + 1):
                    i = '0' + str(i) if i < 10 else str(i)
                    path = f'{ASSET_DIR}/card_backs/{key}_{i}.png'
                    frames.append(pygame.image.load(path))
                self.card_backs[key] = CardBack(frames, data['animation_speed'])

        for key, data in CARD_BACKS.items():
            if data['frames'] == 1:
                path = f'{ASSET_DIR}/card_back_overlays/{key}.png'
                self.card_back_overlays[key] = CardBack([pygame.image.load(path)])
            else:
                frames = []
                for i in range(1, data['frames'] + 1):
                    i = '0' + str(i) if i < 10 else str(i)
                    path = f'{ASSET_DIR}/card_back_overlays/{key}_{i}.png'
                    frames.append(pygame.image.load(path))
                self.card_back_overlays[key] = CardBack(frames, data['animation_speed'])

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

    def draw_card(self, win, key, x, y, selected=False):
        image = self.card_overlays[key] if selected else self.cards[key]
        win.blit(image, (x, y))

    def draw_card_back(self, win, key, x, y, frame_count, selected=False):
        back = self.card_back_overlays[key] if selected else self.card_backs[key]
        back.draw(win, x, y, frame_count)

    def draw_background(self, win, key):
        image = pygame.transform.scale(self.backgrounds[key], (WIN_WIDTH, WIN_HEIGHT))
        win.blit(image, (0, 0))

    def draw_background_select(self, win, key, pos):
        image = pygame.transform.scale(self.backgrounds[key], (100, 100))
        win.blit(image, pos)

    def draw_arrow(self, win, pos, orientation):
        image = pygame.transform.rotate(self.arrow, 180 if orientation == 0 else 0)
        win.blit(image, pos)


class CardBack:
    def __init__(self, frames, animation_speed=None):
        self.frames = frames
        self.animation_speed = animation_speed
        self.curr_frame = 0

    def draw(self, win, x, y, frame_count):
        if len(self.frames) == 1:
            image = self.frames[0]
        else:
            image = self.frames[(frame_count // self.animation_speed) % len(self.frames)]
        win.blit(image, (x, y))


