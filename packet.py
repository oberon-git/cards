def map_to_game(packet, g):
    g.ready = packet.ready
    g.game.turn = packet.turn
    g.game.step = packet.step
    g.game.top = packet.top
    g.game.bottom = packet.bottom
    g.game.deck.curr = packet.curr
    g.game.winner = packet.winner


class Packet:
    def __init__(self, g):
        self.ready = g.ready
        self.turn = g.game.turn
        self.step = g.game.step
        self.top = g.game.top
        self.bottom = g.game.bottom
        self.curr = g.game.deck.curr
        self.winner = g.game.winner
