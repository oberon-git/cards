from src.shared.button import Button
from src.shared.shared_data import WIN_WIDTH, WIN_HEIGHT, CENTER, BUTTON_WIDTH, BUTTON_HEIGHT
from src.shared.shared_data import IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT, BACKGROUND_COUNT
from src.shared.shared_data import CARD_SPACING, CARD_HEIGHT, CARD_WIDTH, CARD_BACKS
from src.shared.game import card_selected


class Menu:
    def __init__(self, settings):
        self.settings = settings
        self.n = 2
        self.play_button = Button(self.get_button_rect(1), "Play", self.play)
        self.continue_button = Button(self.get_button_rect(1), "Continue", self.play, key_triggers=['p'])
        self.selected_game = settings.get_game_name()
        self.game_select_button = Button(self.get_button_rect(2), self.selected_game, self.next_game)
        self.background_select_button = Button(self.get_button_rect(3), "Select Background",
                                               self.select_background_action)
        self.card_select_button = Button(self.get_button_rect(4), "Select Card", self.select_card_action)
        self.back_button = Button((50, WIN_HEIGHT - BUTTON_HEIGHT - 50), "Back", self.back)
        self.pause_button = Button((WIN_WIDTH - 50, 20), None, self.pause, key_triggers=['p'])
        self.back_to_menu_button = Button(self.get_button_rect(2), "Back to Menu", self.back_to_menu)
        self.background_selects = {}
        self.selected_background = None
        self.card_selects = {}
        self.selected_card = None
        self.start = self.active = self.paused = self.exit_game = False
        self.screen = 0

    def get_button_rect(self, x):
        offset = -75 * (self.n - x)
        return CENTER[0] - BUTTON_WIDTH // 2, CENTER[1] + offset - BUTTON_HEIGHT // 2

    def draw(self, win, resources, event, frame_count):
        if self.screen != 2:
            resources.draw_background(win, self.settings.background)
        if self.screen == 0:
            self.play_button.draw(win, resources, event)
            self.game_select_button.draw(win, resources, event)
            self.background_select_button.draw(win, resources, event)
            self.card_select_button.draw(win, resources, event)
        elif self.screen == 1:
            for key, select in self.background_selects.items():
                select.draw(win, resources, event)
            self.back_button.draw(win, resources, event)
        elif self.screen == 2:
            self.pause_button.draw(win, resources, event)
        elif self.screen == 3:
            self.continue_button.draw(win, resources, event)
            self.back_to_menu_button.draw(win, resources, event)
            self.background_select_button.draw(win, resources, event)
            self.card_select_button.draw(win, resources, event)
        elif self.screen == 4:
            for key, pos in self.card_selects.items():
                selected = False
                if card_selected(pos[0], pos[1], event.mouse_pos):
                    selected = True
                    if event.click and key != self.settings.card_back:
                        self.settings.update_card_back(key)
                resources.draw_card_back(win, key, pos[0], pos[1], frame_count,
                                         selected=selected or self.settings.card_back == key)
            self.back_button.draw(win, resources, event)

    def pause(self):
        self.paused = True
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
            if col == images_per_row:
                col = 0
                pos = (spacing, pos[1] + row_offset)
            else:
                pos = (pos[0] + col_offset, pos[1])

    def select_background(self, key):
        self.background_selects[self.settings.background].selected = False
        self.settings.update_background(key)
        self.background_selects[key].selected = True

    def select_card_action(self):
        self.screen = 4
        cards_per_row = 6
        mult = CARD_WIDTH + CARD_SPACING
        offset = (WIN_WIDTH - (cards_per_row * mult) + CARD_SPACING) // 2
        pos = (offset, offset)
        col = 0
        for key in CARD_BACKS.keys():
            self.card_selects[key] = pos
            col += 1
            if col == cards_per_row:
                col = 0
                pos = (offset, pos[1] + CARD_HEIGHT + CARD_SPACING)
            else:
                pos = (pos[0] + mult, pos[1])

    def next_game(self):
        self.settings.next_game()
        self.selected_game = self.settings.get_game_name()
        self.game_select_button.change_text(self.selected_game)

    def back(self):
        if self.paused:
            self.screen = 3
        else:
            self.screen = 0
        self.paused = False

    def back_to_menu(self):
        self.exit_game = True

    def play(self):
        self.start = True
        self.active = False
        self.screen = 2

    def escape(self):
        if self.screen == 0:
            return True
        elif self.screen == 1:
            self.back()
        elif self.screen == 2:
            self.pause()
        elif self.screen == 3:
            self.play()
        elif self.screen == 4:
            self.pause()
        return False
