import pygame
from .shared_data import BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON, OUTLINE_WIDTH, OUTLINE
from .shared_data import IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT, BLACK, FONT_SIZE, FONT_FAMILY


class Button:
    def __init__(self, pos, content, action, selected=False, key_triggers=()):
        self.pos = pos
        self.content = content
        self.action = action
        self.selected = selected
        self.key_triggers = key_triggers
        if type(content) == str:
            self.type = 0
            self.rect = (pos[0], pos[1], BUTTON_WIDTH, BUTTON_HEIGHT)
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

    def draw(self, win, resources, event):
        if self.type == 0:
            self.draw_button(win)
            text = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE).render(self.content, False, BLACK)
            font_rect = text.get_rect()
            font_rect.center = (self.pos[0] + BUTTON_WIDTH // 2, self.pos[1] + BUTTON_HEIGHT // 2)
            win.blit(text, font_rect)
        elif self.type == 1:
            resources.draw_background_select(win, self.key, self.pos)
        elif self.type == 2:
            self.draw_pause_button(win)

        clicked = False
        if self.in_range(event.mouse_pos):
            self.outline(win)
            if event.click:
                clicked = True
                self.click()
        elif self.selected:
            self.outline(win)
        if not clicked and 'p' in self.key_triggers and event.p:
            for trigger in self.key_triggers:
                if event.__getattribute__(trigger):
                    self.click()
                    break

    def change_text(self, text):
        assert self.type == 0
        self.content = text


class TextButton: # TODO inherit from button
    def __init__(self, pos, content, action, selected=False, key_triggers=()):
        # super().__init__(pos, content, action, selected=selected, key_triggers=key_triggers)
        self.pos = pos
        self.content = content
        self.action = action
        self.selected = selected
        self.key_triggers = key_triggers

        self.rect = (pos[0], pos[1], BUTTON_WIDTH, BUTTON_HEIGHT)

    def draw(self, win, resources, event):  # frame_count
        resources.draw_button(win, self.pos)
        text = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE).render(self.content, False, BLACK)
        font_rect = text.get_rect()
        font_rect.center = (self.pos[0] + BUTTON_WIDTH // 2, self.pos[1] + BUTTON_HEIGHT // 2)
        win.blit(text, font_rect)

        clicked = False
        if self.in_range(event.mouse_pos):
            self.outline(win)  # TODO switch out png to highlighted version
            if event.click:
                clicked = True
                self.click()
        elif self.selected:
            self.outline(win)  # TODO switch out png to highlighted version
        if not clicked and 'p' in self.key_triggers and event.p:
            for trigger in self.key_triggers:
                if event.__getattribute__(trigger):
                    self.click()
                    break

    def outline(self, win):
        rect = (self.rect[0] - OUTLINE_WIDTH, self.rect[1] - OUTLINE_WIDTH, self.rect[2] + OUTLINE_WIDTH, self.rect[3] + OUTLINE_WIDTH)
        pygame.draw.rect(win, OUTLINE, rect, width=OUTLINE_WIDTH)

    def click(self):
        self.action()

    def in_range(self, pos):
        if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2]:
            if self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
                return True
        return False
