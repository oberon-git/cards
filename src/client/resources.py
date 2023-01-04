import pygame
import os
from src.shared.shared_data import ASSET_DIR, WIN_WIDTH, WIN_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT
from src.shared.shared_data import CARD_WIDTH, CARD_HEIGHT, CARD_BACKS, IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT


class Resources:
    def __init__(self):
        self.cards = {}
        self.card_backs = {}
        self.backgrounds = {}
        self.ui = {}

        for filename in os.listdir(f'{ASSET_DIR}/cards'):
            path = f'{ASSET_DIR}/cards/{filename}'
            key = filename.replace('_of_', '').replace('.png', '')
            self.cards[key] = pygame.image.load(path)

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

        for filename in os.listdir(f'{ASSET_DIR}/backgrounds'):
            path = f'{ASSET_DIR}/backgrounds/{filename}'
            key = int(filename.replace('backgrounds/', '').replace('.png', ''))
            self.backgrounds[key] = pygame.transform.scale(pygame.image.load(path), (WIN_WIDTH, WIN_HEIGHT))

        for filename in os.listdir(f'{ASSET_DIR}/ui'):
            path = f'{ASSET_DIR}/ui/{filename}'
            key = filename.replace('.png', '')
            self.ui[key] = pygame.image.load(path)

        self.icon = self.ui['icon']
        self.arrow = pygame.transform.rotate(pygame.transform.scale(self.ui['arrow'], (25, 25)), 180)
        self.button = pygame.transform.scale(self.ui['button'], (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.pause_button = self.ui['pause_button']

        self.yellow_overlay = pygame.image.load(f'{ASSET_DIR}/overlays/yellow_overlay.png')
        self.black_overlay = pygame.image.load(f'{ASSET_DIR}/overlays/black_overlay.png')

        self.card_overlay = pygame.transform.scale(self.yellow_overlay, (CARD_WIDTH, CARD_HEIGHT))
        self.new_card_overlay = pygame.transform.scale(self.black_overlay, (CARD_WIDTH, CARD_HEIGHT))
        self.background_overlay = pygame.transform.scale(self.yellow_overlay, (IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT))
        self.button_overlay = pygame.transform.scale(self.yellow_overlay, (BUTTON_WIDTH, BUTTON_HEIGHT))

    def draw_card(self, win, key, x, y, selected=False, new=False):
        image = self.cards[key]
        win.blit(image, (x, y))
        if selected:
            win.blit(self.card_overlay, (x, y))
        elif new:
            win.blit(self.new_card_overlay, (x, y))

    def draw_card_back(self, win, key, x, y, frame_count, selected=False):
        back = self.card_backs[key]
        back.draw(win, x, y, frame_count)
        if selected:
            win.blit(self.card_overlay, (x, y))

    def draw_empty_selection(self, win, x, y):
        win.blit(self.card_overlay, (x, y))

    def draw_background(self, win, key):
        image = self.backgrounds[key]
        win.blit(image, (0, 0))

    def draw_background_select(self, win, key, pos, selected=False):
        image = pygame.transform.scale(self.backgrounds[key], (IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT))
        win.blit(image, pos)
        if selected:
            win.blit(self.background_overlay, pos)

    def draw_arrow(self, win, pos, orientation):
        image = pygame.transform.rotate(self.arrow, 180 if orientation == 0 else 0)
        win.blit(image, pos)

    def draw_button(self, win, pos, selected=False):
        win.blit(self.button, pos)
        if selected:
            win.blit(self.button_overlay, pos)

    def draw_pause_button(self, win, pos):
        win.blit(self.pause_button, pos)


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


