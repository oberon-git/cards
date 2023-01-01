import os
import yaml
from src.shared.shared_data import USER_SETTINGS_PATH, DEFAULT_USER_SETTINGS, GAMES


class UserSettings:
    def __init__(self):
        if not os.path.exists(USER_SETTINGS_PATH):
            with open(USER_SETTINGS_PATH, 'w') as user_file:
                yaml.dump(DEFAULT_USER_SETTINGS, user_file)
            self.settings = DEFAULT_USER_SETTINGS
        else:
            with open(USER_SETTINGS_PATH, 'r') as user_file:
                self.settings = yaml.safe_load(user_file)
                for key, val in DEFAULT_USER_SETTINGS.items():
                    if key not in self.settings:
                        self.settings[key] = val
            with open(USER_SETTINGS_PATH, 'w') as user_file:
                yaml.dump(self.settings, user_file)
        self.background = self.settings["background"]
        self.card_back = self.settings["card_back"]
        self.game = self.settings["game"]

    def get_game_name(self):
        return GAMES[self.game]

    def next_game(self):
        self.game += 1
        if self.game not in GAMES:
            self.game = 1
        self.settings["game"] = self.game
        self.update()

    def update_card_back(self, card_back):
        self.settings["card_back"] = card_back
        self.update()
        self.card_back = self.settings["card_back"]

    def update_background(self, background):
        self.settings["background"] = background
        self.update()
        self.background = self.settings["background"]

    def update(self):
        with open(USER_SETTINGS_PATH, 'w') as user_file:
            yaml.dump(self.settings, user_file)
        with open(USER_SETTINGS_PATH, 'r') as user_file:
            self.settings = yaml.safe_load(user_file)
