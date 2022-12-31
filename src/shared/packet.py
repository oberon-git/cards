from .threading_funcs import synchronized


@synchronized
def map_to_game(packet, game):
    game.turn = packet.turn
    game.step = packet.step
    game.top_card = packet.top_card
    game.bottom_card = packet.bottom_card
    game.deck.curr = packet.curr
    game.winner = packet.winner
    game.reset = packet.reset
    game.over = packet.over
    game.players = packet.players
    game.new_card_index = packet.new_card_index


class Packet:
    def __init__(self, game):
        self.turn = game.turn
        self.step = game.step
        self.top = game.top_card
        self.bottom = game.bottom_card
        self.curr = game.deck.curr
        self.winner = game.winner
        self.reset = game.reset
        self.over = game.over
        self.players = game.players
        self.new_card_index = game.new_card_index
