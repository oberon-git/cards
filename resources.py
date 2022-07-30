import pygame


class Resources:
    def __init__(self, file_list):
        self.cards = {}
        self.backgrounds = {}
        for filename in file_list:
            if "cards" in filename:
                key = filename.replace("assets/cards/", "").replace("_of_", "").replace(".png", "")
                self.cards[key] = pygame.image.load(filename)
            elif "backgrounds" in filename:
                key = int(filename.replace("assets/backgrounds/", "").replace(".png", ""))
                self.backgrounds[key] = pygame.image.load(filename)

    def draw_card(self, win, key, x, y):
        image = self.cards[key]
        win.blit(image, (x, y))

    def draw_background(self, win, key):
        image = pygame.transform.scale(self.backgrounds[key], (win.get_width(), win.get_height()))
        win.blit(image, (0, 0))

