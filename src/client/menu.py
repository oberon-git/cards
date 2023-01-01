from src.shared.button import Button
from src.shared.shared_data import WIN_WIDTH, WIN_HEIGHT, CENTER, BUTTON_WIDTH, BUTTON_HEIGHT
from src.shared.shared_data import IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT, BACKGROUND_COUNT
from src.shared.shared_data import CARD_SPACING, CARD_HEIGHT, CARD_WIDTH, CARD_BACKS
from src.shared.game import card_selected


def get_button_rect(x):
    offset = -75 * (2 - x)
    return CENTER[0] - BUTTON_WIDTH // 2, CENTER[1] + offset - BUTTON_HEIGHT // 2


class Menu:
    def __init__(self, settings):
        self.settings = settings

        self.menus = {
            'main': {
                'screen': 0,
                'buttons': []
            },
            'background_select': {
                'screen': 1,
                'buttons': []
            },
            'card_select': {
                'screen': 2,
                'buttons': []
            },
            'game': {
                'screen': 3,
                'buttons': []
            },
            'pause': {
                'screen': 4,
                'buttons': []
            }
        }

        self.play_button = Button(get_button_rect(1), "Play", self.play)
        self.continue_button = Button(get_button_rect(1), "Continue", self.play, key_triggers='p')
        self.selected_game = settings.get_game_name()
        self.game_select_button = Button(get_button_rect(2), self.selected_game, self.next_game)
        self.background_select_button = Button(get_button_rect(3), "Select Background",
                                               self.background_select_action())
        self.card_select_button = Button(get_button_rect(4), "Select Card", self.select_card_action)
        self.back_button = Button((50, WIN_HEIGHT - BUTTON_HEIGHT - 50), "Back", self.back)
        self.pause_button = Button((WIN_WIDTH - 50, 20), None, self.pause, key_triggers='p')
        self.back_to_menu_button = Button(get_button_rect(2), "Back to Menu", self.back_to_menu)
        self.background_selects = self.build_background_selects()
        self.background_selects.append(self.back_button)
        self.card_selects = {}

        self.menus['main']['buttons'].extend([
            self.play_button,
            self.game_select_button,
            self.background_select_button,
            self.card_select_button
        ])
        self.menus['background_select']['buttons'].extend([
            self.background_selects
        ])
        self.menus['card_select']['buttons'].extend([
            self.back_button
        ])
        self.menus['game']['buttons'].extend([
            self.pause_button
        ])
        self.menus['pause']['buttons'].extend([
            self.continue_button,
            self.back_to_menu_button,
            self.background_select_button,
            self.card_select_button
        ])

        self.screen = self.menus['main']['screen']
        self.start = self.active = self.exit_game = False

    def draw(self, win, resources, event, frame_count):
        if self.screen == self.menus['main']['screen']:
            resources.draw_background(win, self.settings.background)
            for button in self.menus['main']['buttons']:
                button.draw(win, resources, event)
        elif self.screen == self.menus['background_select']['screen']:
            resources.draw_background(win, self.settings.background)
            for button in self.menus['background_select']['buttons']:
                button.draw(win, resources, event)
        elif self.screen == self.menus['card_select']['screen']:
            resources.draw_background(win, self.settings.background)
            for key, pos in self.card_selects.items():
                selected = False
                if card_selected(pos[0], pos[1], event.mouse_pos):
                    selected = True
                    if event.click and key != self.settings.card_back:
                        self.settings.update_card_back(key)
                resources.draw_card_back(win, key, pos[0], pos[1], frame_count,
                                         selected=selected or self.settings.card_back == key)
            for button in self.menus['card_select']['buttons']:
                button.draw(win, resources, event)
        elif self.screen == self.menus['game']['screen']:
            for button in self.menus['game']['buttons']:
                button.draw(win, resources, event)
        elif self.screen == self.menus['pause']['screen']:
            resources.draw_background(win, self.settings.background)
            for button in self.menus['pause']['buttons']:
                button.draw(win, resources, event)

    def pause(self):
        self.screen = self.menus['pause']['screen']
        self.active = True

    def background_select_action(self):
        self.screen = self.menus['background_select']['screen']

    def build_background_selects(self):
        images_per_row = 4
        spacing = (WIN_WIDTH - images_per_row * IMAGE_BUTTON_WIDTH) // (images_per_row + 1)
        col_offset = IMAGE_BUTTON_WIDTH + spacing
        row_offset = IMAGE_BUTTON_HEIGHT + spacing
        pos = (spacing, spacing)
        col = 0
        background_selects = []
        for i in range(1, BACKGROUND_COUNT + 1):
            selected = i == self.settings.background
            background_selects.append(Button(pos, i, self.select_background, selected))
            col += 1
            if col == images_per_row:
                col = 0
                pos = (spacing, pos[1] + row_offset)
            else:
                pos = (pos[0] + col_offset, pos[1])
        return background_selects

    def select_background(self, key):
        self.background_selects[self.settings.background].selected = False
        self.settings.update_background(key)
        self.background_selects[key].selected = True

    def select_card_action(self):
        self.screen = self.menus['card_select']['screen']
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
        if self.start:
            self.screen = self.menus['pause']['screen']
        else:
            self.screen = self.menus['main']['screen']

    def back_to_menu(self):
        self.exit_game = True

    def play(self):
        self.start = True
        self.active = False
        self.screen = self.menus['game']['screen']

    def escape(self):
        if self.screen == self.menus['main']['screen']:
            return True
        elif self.screen == self.menus['background_select']['screen']:
            self.back()
        elif self.screen == self.menus['card_select']['screen']:
            self.back()
        elif self.screen == self.menus['game']['screen']:
            self.pause()
        elif self.screen == self.menus['pause']['screen']:
            self.play()
        return False
