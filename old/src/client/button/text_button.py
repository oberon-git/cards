import pygame
from src.shared.shared_data import BUTTON_WIDTH, BUTTON_HEIGHT, BLINK_SPEED, BLACK, FONT_SIZE, FONT_FAMILY
from .button import Button


class TextButton(Button):
    def __init__(self, pos, content, action, selected=False, key_triggers=()):
        super().__init__(pos, content, action, selected=selected, key_triggers=key_triggers)
        self.rect = (pos[0], pos[1], BUTTON_WIDTH, BUTTON_HEIGHT)
        self.text = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE).render(self.content, False, BLACK)
        self.font_rect = self.text.get_rect()
        self.font_rect.center = (self.pos[0] + BUTTON_WIDTH // 2, self.pos[1] + BUTTON_HEIGHT // 2)

    def draw(self, win, resources, event, frame_count):  # frame_count
        selected = False
        if self.in_range(event.mouse_pos):
            selected = True
            if event.click or event.enter:
                self.click()
        elif self.selected:
            selected = True
            if event.enter:
                self.click()

        resources.draw_button(win, self.pos, selected=selected)
        win.blit(self.text, self.font_rect)

    def set_text(self, text):
        self.content = text
        self.text = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE).render(self.content, False, BLACK)
        self.font_rect = self.text.get_rect()
        self.font_rect.center = (self.pos[0] + BUTTON_WIDTH // 2, self.pos[1] + BUTTON_HEIGHT // 2)
