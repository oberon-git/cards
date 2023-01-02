from .shared_data import CARD_WIDTH, CARD_HEIGHT, CENTER, BLINK_SPEED, CARD_SPACING, WIN_WIDTH, WIN_HEIGHT, BLACK
from .game import Game, card_selected, outline_card


class Rummy(Game):
    def __init__(self):
        super().__init__(7)
        self.step = 0
        self.top_card = self.deck.deal_card()
        self.bottom_card = None
        self.new_card_index = -1

    def draw(self, win, resources, client_data, p, event, frame_count, network):
        super().draw(win, resources, client_data, p, event, frame_count, network)

        select_frame = (frame_count // (BLINK_SPEED * 2)) % 2 == 0
        mult = CARD_WIDTH + CARD_SPACING
        offset = (WIN_WIDTH - (len(self.players[p].hand()) * mult) + CARD_SPACING) // 2
        hand = self.players[p].hand()

        if self.turn == p and not self.over:
            if self.step == 0:
                if event.left:
                    if client_data.selected_index > 0:
                        client_data.selected_index -= 1
                elif event.right:
                    if client_data.selected_index < 1:
                        client_data.selected_index += 1
            elif self.step == 1:
                if event.left:
                    if client_data.selected_index > 0:
                        client_data.selected_index -= 1
                elif event.right:
                    if client_data.selected_index < self.hand_size:
                        client_data.selected_index += 1

        # draw the players hand
        y = WIN_HEIGHT - CARD_HEIGHT - 30
        for i in range(len(hand)):
            c = hand[i]
            x = i * mult + offset
            selected = False
            if self.turn == p and self.step == 1 and not self.over:
                if card_selected(x, y, event.mouse_pos):
                    client_data.selected_index = i
                    selected = True
                    if event.click or event.enter:
                        network.send_command_to_server(DiscardCommand(p, c))
                        client_data.selected_index = 0
                elif i == client_data.selected_index:
                    selected = True
                    if event.enter:
                        network.send_command_to_server(DiscardCommand(p, c))
                        client_data.selected_index = 0
                elif self.turn == p and self.step == 1 and not self.over and self.new_card_index == i:
                    if (frame_count // (BLINK_SPEED * 2)) % 2 == 0:
                        outline_card(win, x, y, BLACK)
            c.draw(win, resources, x, y, selected=selected and select_frame)

        # draw the opponents hand
        if self.over:
            o = 1 - p
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
                resources.draw_card_back(win, client_data.settings.card_back, i * mult + offset, 30, frame_count)

        # draw deck and discard piles
        x = CENTER[0] - CARD_WIDTH // 2 - mult // 2
        y = CENTER[1] - CARD_HEIGHT // 2
        if not self.deck.is_empty():
            selected = False
            if self.turn == p and self.step == 0 and not self.over:
                if card_selected(x, y, event.mouse_pos):
                    client_data.selected_index = 0
                    selected = True
                    if event.click or event.enter:
                        network.send_command_to_server(DrawFromDeckCommand(p))
                        client_data.selected_index = 0
                elif client_data.selected_index == 0:
                    selected = True
                    if event.enter:
                        network.send_command_to_server(DrawFromDeckCommand(p))
                        client_data.selected_index = 0
            resources.draw_card_back(win, client_data.settings.card_back, x, y, frame_count, selected=selected and select_frame)
        x += mult
        if self.over:
            resources.draw_card_back(win, client_data.settings.card_back, x, y, frame_count)
        elif self.top_card is not None:
            selected = False
            if self.turn == p and self.step == 0:
                if card_selected(x, y, event.mouse_pos):
                    client_data.selected_index = 1
                    selected = True
                    if event.click or event.enter:
                        network.send_command_to_server(DrawFromDiscardCommand(p))
                        client_data.selected_index = 0
                elif client_data.selected_index == 1:
                    selected = True
                    if event.enter:
                        network.send_command_to_server(DrawFromDiscardCommand(p))
                        client_data.selected_index = 0
            self.top_card.draw(win, resources, x, y, selected=selected and select_frame)

    def draw_card_from_deck(self, p):
        c = self.deck.deal_card()
        self.new_card_index = self.players[p].draw_card(c)
        if self.deck.is_empty():
            self.winner = 2
            self.over = True
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
