from src.shared.button import Button
from src.shared.shared_data import *


class Menu:
    def __init__(self, settings, paused=False):
        self.settings = settings
        self.paused = paused
        self.n = 2
        self.play_button = Button(self.get_button_rect(1), "Continue" if self.paused else "Play", self.play)
        self.background_select_button = Button(self.get_button_rect(2), "Select Background",
                                               self.select_background_action)
        self.back_button = Button((50, WIN_HEIGHT - BUTTON_HEIGHT - 50), "Back", self.back)
        self.pause_button = Button((WIN_WIDTH - 50, 20), None, self.pause)
        self.background_selects = {}
        self.selected_background = None
        self.start = self.active = False
        self.screen = 2 if self.paused else 0

    def get_button_rect(self, x):
        offset = -75 * (self.n - x)
        return CENTER[0] - BUTTON_WIDTH // 2, CENTER[1] + offset - BUTTON_HEIGHT // 2

    def draw(self, win, resources, clicked, mouse_pos):
        if self.screen != 2:
            resources.draw_background(win, self.settings.background)
        if self.screen == 0:
            self.play_button.draw(win, mouse_pos, clicked, resources)
            self.background_select_button.draw(win, mouse_pos, clicked, resources)
        elif self.screen == 1:
            for key, select in self.background_selects.items():
                select.draw(win, mouse_pos, clicked, resources)
            self.back_button.draw(win, mouse_pos, clicked, resources)
        elif self.screen == 2:
            self.pause_button.draw(win, mouse_pos, clicked, resources)
        elif self.screen == 3:
            self.play_button.draw(win, mouse_pos, clicked, resources)
            self.background_select_button.draw(win, mouse_pos, clicked, resources)

    def pause(self):
        self.screen = 3
        self.active = True

    def select_background_action(self):
        self.screen = 1
        images_per_row = 4
        spacing = (WIN_WIDTH - images_per_row * IMAGE_BUTTON_WIDTH) // (images_per_row + 1)
        col_offset = IMAGE_BUTTON_WIDTH + spacing
        row_offset = IMAGE_BUTTON_HEIGHT + spacing
        pos = (spacing, spacing)
        col = 0
        for i in range(1, BACKGROUND_COUNT + 1):
            selected = i == self.settings.background
            self.background_selects[i] = (Button(pos, i, self.select_background, selected))
            col += 1
            if col == 4:
                col = 0
                pos = (spacing, pos[1] + row_offset)
            else:
                pos = (pos[0] + col_offset, pos[1])

    def select_background(self, key):
        self.background_selects[self.settings.background].selected = False
        self.settings.update_background(key)
        self.background_selects[key].selected = True

    def back(self):
        self.screen = 3 if self.paused else 0

    def play(self):
        self.start = True
        if self.paused:
            self.active = False
            self.screen = 2

    def escape(self, escaped=True):
        if escaped:
            if self.screen == 0:
                return False
            elif self.screen == 1:
                self.back()
            elif self.screen == 2:
                self.pause()
            elif self.screen == 3:
                self.play()
        return True
