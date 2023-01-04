from .button.text_button import TextButton
from .button.pause_button import PauseButton
from .button.background_select_button import BackgroundSelectButton
from .button.card_select_button import CardSelectButton
from .button.button import Button
from src.shared.shared_data import WIN_WIDTH, WIN_HEIGHT, CENTER, BUTTON_WIDTH, BUTTON_HEIGHT
from src.shared.shared_data import IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT, BACKGROUND_COUNT
from src.shared.shared_data import CARD_SPACING, CARD_HEIGHT, CARD_WIDTH, CARD_BACKS


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

        self.play_button = TextButton(get_button_rect(1), "Play", self.play)
        self.continue_button = TextButton(get_button_rect(1), "Continue", self.play, key_triggers='p')

        self.selected_game = settings.get_game_name()
        self.game_select_button = TextButton(get_button_rect(2), self.selected_game, self.next_game)

        self.background_select_button = TextButton(get_button_rect(3), "Select Background",
                                                   self.background_select_action)
        self.card_select_button = TextButton(get_button_rect(4), "Select Card", self.select_card_action)

        self.pause_button = PauseButton((WIN_WIDTH - 50, 20), self.pause, key_triggers='p')
        self.play_again_button = TextButton((CENTER[0] - BUTTON_WIDTH // 2, CENTER[1] + 100), "Play Again", self.play_again)

        self.back_button = TextButton((50, WIN_HEIGHT - BUTTON_HEIGHT - 50), "Back", self.back)
        self.back_to_menu_button = TextButton(get_button_rect(2), "Back to Menu", self.back_to_menu)

        self.images_per_row = 4
        self.cards_per_row = 6
        self.background_selects = self.build_background_selects()
        self.background_selects.append(self.back_button)
        self.card_selects = self.build_card_selects()

        self.menus['main']['buttons'].extend([
            self.play_button,
            self.game_select_button,
            self.background_select_button,
            self.card_select_button
        ])
        self.menus['background_select']['buttons'].extend(
            self.background_selects
        )
        self.menus['card_select']['buttons'].extend(
            list(self.card_selects.values())
        )
        self.menus['card_select']['buttons'].extend([
            self.back_button
        ])
        self.menus['game']['buttons'].extend([
            self.pause_button,
            self.play_again_button
        ])
        self.menus['pause']['buttons'].extend([
            self.continue_button,
            self.back_to_menu_button,
            self.background_select_button,
            self.card_select_button
        ])

        self.screen = self.menus['main']['screen']
        self.start = self.active = self.exit_game = False
        self.selected_button_index = 0

    def draw(self, win, resources, event, frame_count, game_over=False):
        if self.screen == self.menus['main']['screen']:
            resources.draw_background(win, self.settings.background)
            self.set_selected_button(event, self.menus['main']['buttons'])
            for i, button in enumerate(self.menus['main']['buttons']):
                button.selected = i == self.selected_button_index
                button.draw(win, resources, event, frame_count)
        elif self.screen == self.menus['background_select']['screen']:
            resources.draw_background(win, self.settings.background)
            selected = False
            for i, button in enumerate(self.menus['background_select']['buttons']):
                if button.in_range(event.mouse_pos):
                    selected = True
                    self.selected_button_index = i
            if not selected:
                if event.right:
                    if self.selected_button_index < len(self.menus['background_select']['buttons']) - 1:
                        self.selected_button_index += 1
                elif event.left:
                    if self.selected_button_index > 0:
                        self.selected_button_index -= 1
                elif event.down:
                    if self.selected_button_index < len(self.menus['background_select']['buttons']) - self.images_per_row - 1:
                        self.selected_button_index += self.images_per_row
                    elif self.selected_button_index != len(self.menus['background_select']['buttons']) - 1:
                        self.selected_button_index = len(self.menus['background_select']['buttons']) - 1
                elif event.up:
                    if self.selected_button_index == len(self.menus['background_select']['buttons']) - 1:
                        self.selected_button_index -= 1
                    elif self.selected_button_index >= self.images_per_row:
                        self.selected_button_index -= self.images_per_row
            for i, button in enumerate(self.menus['background_select']['buttons']):
                button.selected = i + 1 == self.settings.background or i == self.selected_button_index
                button.draw(win, resources, event, frame_count)
        elif self.screen == self.menus['card_select']['screen']:
            resources.draw_background(win, self.settings.background)
            selected = False
            for i, button in enumerate(self.menus['card_select']['buttons']):
                if button.in_range(event.mouse_pos):
                    selected = True
                    self.selected_button_index = i
            if not selected:
                if event.right:
                    if self.selected_button_index < len(self.menus['card_select']['buttons']) - 1:
                        self.selected_button_index += 1
                elif event.left:
                    if self.selected_button_index > 0:
                        self.selected_button_index -= 1
                elif event.down:
                    if self.selected_button_index < len(self.menus['card_select']['buttons']) - self.cards_per_row - 1:
                        self.selected_button_index += self.cards_per_row
                    elif self.selected_button_index != len(self.menus['card_select']['buttons']) - 1:
                        self.selected_button_index = len(self.menus['card_select']['buttons']) - 1
                elif event.up:
                    if self.selected_button_index == len(self.menus['card_select']['buttons']) - 1:
                        self.selected_button_index -= 1
                    elif self.selected_button_index >= self.cards_per_row:
                        self.selected_button_index -= self.cards_per_row
            for i, button in enumerate(self.menus['card_select']['buttons']):
                button.selected = i == self.selected_button_index or button.content == self.settings.card_back
                button.draw(win, resources, event, frame_count)
        elif self.screen == self.menus['game']['screen']:
            self.pause_button.draw(win, resources, event, frame_count)
            if game_over:
                self.play_again_button.selected = True
                self.play_again_button.draw(win, resources, event, frame_count)
        elif self.screen == self.menus['pause']['screen']:
            resources.draw_background(win, self.settings.background)
            self.set_selected_button(event, self.menus['pause']['buttons'])
            for i, button in enumerate(self.menus['pause']['buttons']):
                button.selected = i == self.selected_button_index
                button.draw(win, resources, event, frame_count)

    def set_selected_button(self, event, buttons):
        for i, button in enumerate(buttons):
            if button.in_range(event.mouse_pos):
                self.selected_button_index = i
                return
        if event.down:
            if self.selected_button_index < len(buttons) - 1:
                self.selected_button_index += 1
        elif event.up:
            if self.selected_button_index > 0:
                self.selected_button_index -= 1

    def pause(self):
        self.screen = self.menus['pause']['screen']
        self.active = True
        self.selected_button_index = 0

    def background_select_action(self):
        self.screen = self.menus['background_select']['screen']
        self.selected_button_index = 0

    def build_background_selects(self) -> list[Button]:
        spacing = (WIN_WIDTH - self.images_per_row * IMAGE_BUTTON_WIDTH) // (self.images_per_row + 1)
        col_offset = IMAGE_BUTTON_WIDTH + spacing
        row_offset = IMAGE_BUTTON_HEIGHT + spacing
        pos = (spacing, spacing)
        col = 0
        background_selects = []
        for i in range(BACKGROUND_COUNT):
            selected = i + 1 == self.settings.background
            background_selects.append(BackgroundSelectButton(pos, i + 1, self.select_background, selected=selected))
            col += 1
            if col == self.images_per_row:
                col = 0
                pos = (spacing, pos[1] + row_offset)
            else:
                pos = (pos[0] + col_offset, pos[1])
        return background_selects

    def select_background(self, key):
        self.background_selects[self.settings.background].selected = False
        self.settings.update_background(key)
        self.background_selects[key].selected = True

    def build_card_selects(self):
        mult = CARD_WIDTH + CARD_SPACING
        offset = (WIN_WIDTH - (self.cards_per_row * mult) + CARD_SPACING) // 2
        pos = (offset, offset)
        col = 0
        card_selects = {}
        for key in CARD_BACKS.keys():
            selected = key == self.settings.card_back
            card_selects[key] = CardSelectButton(pos, key, self.select_card, selected=selected)
            col += 1
            if col == self.cards_per_row:
                col = 0
                pos = (offset, pos[1] + CARD_HEIGHT + CARD_SPACING)
            else:
                pos = (pos[0] + mult, pos[1])
        return card_selects

    def select_card_action(self):
        self.screen = self.menus['card_select']['screen']
        self.selected_button_index = 0

    def select_card(self, key):
        self.card_selects[self.settings.card_back].selected = False
        self.settings.update_card_back(key)
        self.card_selects[key].selected = True

    def next_game(self):
        self.settings.next_game()
        self.selected_game = self.settings.get_game_name()
        self.game_select_button.set_text(self.selected_game)

    def back(self):
        if self.start:
            self.screen = self.menus['pause']['screen']
        else:
            self.screen = self.menus['main']['screen']
        self.selected_button_index = 0

    def back_to_menu(self):
        self.exit_game = True

    def play(self):
        self.start = True
        self.active = False
        self.screen = self.menus['game']['screen']
        self.selected_button_index = 0

    def play_again(self):
        self.exit_game = True

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
