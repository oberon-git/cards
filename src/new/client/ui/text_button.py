import pygame

TEXT_BUTTON_WIDTH = 200
TEXT_BUTTON_HEIGHT = 35


class TextButton:
    def __init__(self, win, pos, text, onclick, selected=False):
        self.win = win
        self.pos = pos
        self.text = text
        self.click = onclick
        self.selected = selected

        self.rect = (pos[0], pos[1], TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)
        self.font = pygame.font.SysFont('Times', 30)
        self.text = self.font.render(text, False, (0, 0, 0))
        self.font_rect = self.text.get_rect()
        self.font_rect.center = (pos[0] + TEXT_BUTTON_WIDTH // 2, pos[1] + TEXT_BUTTON_HEIGHT // 2)

    def draw(self, mouse_pos, clicked):
        pygame.draw.rect(self.win, pygame.color.Color((200, 200, 200)), self.rect)
        self.win.blit(self.text, self.font_rect)
        if self.in_range(mouse_pos):
            self.outline()
            if clicked:
                self.click()
        elif self.selected:
            self.outline()

    def outline(self):
        rect = (self.rect[0] - 2, self.rect[1] - 2, self.rect[2] + 2, self.rect[3] + 2)
        pygame.draw.rect(self.win, pygame.color.Color((255, 255, 0)), rect, width=2)

    def in_range(self, pos):
        if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2]:
            if self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
                return True
        return False
