from rummy import Rummy


def get_game(game):
    if game == "rummy":
        return Rummy()


class Game:
    def __init__(self, game):
        self.game = get_game(game)
        self.ready = False

    def draw(self, win, resources, p, mouse_pos, clicked):
        self.game.draw(win, resources, p, mouse_pos, clicked)

    def connected(self):
        return self.ready

    def connect(self):
        self.ready = True


