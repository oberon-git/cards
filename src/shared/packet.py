from .threading_funcs import synchronized


@synchronized
def map_to_game(packet, game):
    game.turn = packet.turn
    game.step = packet.step
    game.top = packet.top
    game.bottom = packet.bottom
    game.deck.curr = packet.curr
    game.winner = packet.winner
    game.reset = packet.reset
    game.over = packet.over
    game.players = packet.players


class Packet:
    def __init__(self, game):
        self.turn = game.turn
        self.step = game.step
        self.top = game.top
        self.bottom = game.bottom
        self.curr = game.deck.curr
        self.winner = game.winner
        self.reset = game.reset
        self.over = game.over
        self.players = game.players
