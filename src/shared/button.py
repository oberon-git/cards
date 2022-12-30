import pygame
from .shared_data import *


if not pygame.get_init():
    pygame.init()


class Button:
    def __init__(self, pos, content, action, selected=False):
        self.pos = pos
        self.action = action
        self.selected = selected
        if type(content) == str:
            self.type = 0
            self.rect = (pos[0], pos[1], BUTTON_WIDTH, BUTTON_HEIGHT)
            self.text = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE).render(content, False, BLACK)
            self.font_rect = self.text.get_rect()
            self.font_rect.center = (pos[0] + BUTTON_WIDTH // 2, pos[1] + BUTTON_HEIGHT // 2)
        if type(content) == int:
            self.type = 1
            self.rect = (pos[0], pos[1], IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT)
            self.key = content
        if content is None:
            self.type = 2
            self.rect = (self.pos[0], self.pos[1], 30, 40)

    def outline(self, win):
        if self.type != 2:
            rect = (self.rect[0] - OUTLINE_WIDTH, self.rect[1] - OUTLINE_WIDTH, self.rect[2] + OUTLINE_WIDTH, self.rect[3] + OUTLINE_WIDTH)
            pygame.draw.rect(win, OUTLINE, rect, width=OUTLINE_WIDTH)

    def in_range(self, pos):
        if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2]:
            if self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
                return True
        return False

    def click(self):
        if self.type == 1:
            self.action(self.key)
        else:
            self.action()

    def draw_button(self, win):
        pygame.draw.rect(win, BUTTON, self.rect)

    def draw_pause_button(self, win):
        pygame.draw.rect(win, BLACK, (self.pos[0], self.pos[1], 10, 40))
        pygame.draw.rect(win, BLACK, (self.pos[0] + 20, self.pos[1], 10, 40))

    def draw(self, win, mouse_pos, clicked, resources):
        if self.type == 0:
            self.draw_button(win)
            win.blit(self.text, self.font_rect)
        elif self.type == 1:
            resources.draw_background_select(win, self.key, self.pos)
        elif self.type == 2:
            self.draw_pause_button(win)
        if self.in_range(mouse_pos):
            self.outline(win)
            if clicked:
                self.click()
        elif self.selected:
            self.outline(win)

    def change_text(self, text):
        assert self.type == 0
        self.text = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE).render(text, False, BLACK)
        self.font_rect = self.text.get_rect()
        self.font_rect.center = (self.pos[0] + BUTTON_WIDTH // 2, self.pos[1] + BUTTON_HEIGHT // 2)
