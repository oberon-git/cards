from .shared_data import CARD_WIDTH, CARD_HEIGHT, CENTER, BLINK_SPEED, CARD_SPACING, WIN_WIDTH, WIN_HEIGHT, BLACK
from .game import Game, card_selected, outline_card


class Rummy(Game):
    def __init__(self):
        super().__init__(7)
        self.step = 0
        self.top_card = self.deck.deal_card()
        self.bottom_card = None
        self.new_card_index = -1

    def draw(self, win, resources, settings, p, mouse_pos, clicked, count, network):
        super().draw(win, resources, settings, p, mouse_pos, clicked, count, network)

        back = "castle_back_0" + str(((count // BLINK_SPEED) % 2) + 1)
        mult = CARD_WIDTH + CARD_SPACING
        offset = (WIN_WIDTH - (len(self.players[p].hand()) * mult) + CARD_SPACING) // 2
        hand = self.players[p].hand()

        for i in range(len(hand)):
            c = hand[i]
            x = i * mult + offset
            y = WIN_HEIGHT - CARD_HEIGHT - 30
            c.draw(win, resources, x, y)
            if self.turn == p and self.step == 1 and not self.over and card_selected(x, y, mouse_pos):
                outline_card(win, x, y)
                if clicked:
                    network.send_command_to_server(DiscardCommand(p, c))
            elif self.turn == p and self.step == 1 and not self.over and self.new_card_index == i:
                if (count // BLINK_SPEED) % 2 == 0:
                    outline_card(win, x, y, BLACK)

        if self.over:
            o = 0 if p == 1 else 1
            hand = self.players[o].hand()
            for i in range(len(hand)):
                c = hand[i]
                x = i * mult + offset
                y = 30
                c.draw(win, resources, x, y)
        else:
            n = self.hand_size + 1 if self.turn != p and self.step == 1 else self.hand_size
            offset = (WIN_WIDTH - (n * mult) + CARD_SPACING) // 2
            for i in range(n):
                resources.draw_card(win, back, i * mult + offset, 30)

        x = CENTER[0] - CARD_WIDTH // 2 - mult // 2
        y = CENTER[1] - CARD_HEIGHT // 2
        resources.draw_card(win, back, x, y)
        if self.turn == p and self.step == 0 and not self.over and card_selected(x, y, mouse_pos):
            outline_card(win, x, y)
            if clicked:
                network.send_command_to_server(DrawFromDeckCommand(p))
        x += mult
        if self.over:
            resources.draw_card(win, back, x, y)
        elif self.top_card is not None:
            resources.draw_card(win, self.top_card.card(), x, y)
            if self.turn == p and self.step == 0 and card_selected(x, y, mouse_pos):
                outline_card(win, x, y)
                if clicked:
                    network.send_command_to_server(DrawFromDiscardCommand(p))

    def draw_card_from_deck(self, p):
        self.new_card_index = self.players[p].draw_card(self.deck.deal_card())
        self.step = 1

    def draw_top_card(self, p):
        self.new_card_index = self.players[p].draw_card(self.top_card)
        self.top_card = self.bottom_card
        self.bottom_card = None
        self.step = 1

    def discard_card(self, p, c):
        self.players[p].play_card(c)
        if self.players[p].won():
            self.winner = p
            self.over = True
        self.bottom_card = self.top_card
        self.top_card = c
        self.step = 0
        self.turn = 1 - self.turn


class DrawFromDeckCommand:
    def __init__(self, p):
        self.p = p

    def run(self, game):
        game.draw_card_from_deck(self.p)


class DrawFromDiscardCommand:
    def __init__(self, p):
        self.p = p

    def run(self, game):
        game.draw_top_card(self.p)


class DiscardCommand:
    def __init__(self, p, card):
        self.p = p
        self.card = card

    def run(self, game):
        game.discard_card(self.p, self.card)
