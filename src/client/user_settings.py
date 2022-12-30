from src.shared.shared_data import *


class UserSettings:
    def __init__(self):
        with open(USER_SETTINGS_PATH, 'r') as user_file:
            self.settings = yaml.safe_load(user_file)
        self.background = self.settings["background"]
        self.game = self.settings["game"]

    def get_game_name(self):
        return GAMES[self.game]

    def update_background(self, background):
        self.settings["background"] = background
        self.update()
        self.background = self.settings["background"]

    def update(self):
        with open(USER_SETTINGS_PATH, 'w') as user_file:
            yaml.dump(self.settings, user_file)
        with open(USER_SETTINGS_PATH, 'r') as user_file:
            self.settings = yaml.safe_load(user_file)

