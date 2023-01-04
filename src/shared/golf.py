from .shared_data import CARD_WIDTH, CARD_HEIGHT, CENTER, BLINK_SPEED, CARD_SPACING, WIN_WIDTH, WIN_HEIGHT
from .game import Game, card_selected


class Golf(Game):
    def __init__(self):
        super().__init__(6)
        self.step = 0
        self.top_card = self.deck.deal_card()
        self.bottom_card = None
        self.drawn_card = None

    def draw(self, win, resources, client_data, p, event, frame_count, network):
        super().draw(win, resources, client_data, p, event, frame_count, network)

        select_frame = (frame_count // (BLINK_SPEED * 2)) % 2 == 0
        mult = CARD_WIDTH + CARD_SPACING
        offset = (WIN_WIDTH - (3 * mult) + CARD_SPACING) // 2
        o = 1 - p
        hand = self.players[p].hand()
        opponents_hand = self.players[o].hand()

        if self.turn == p and not self.over:
            if self.step == 0:
                if event.left:
                    if client_data.selected_index > 0:
                        client_data.selected_index -= 1
                elif event.right:
                    if client_data.selected_index < 1:
                        client_data.selected_index += 1
            elif self.step == 1 or self.step == 2:  # TODO fix movement rules for step 2
                if event.left:
                    if client_data.selected_index > 0 and client_data.selected_index != self.hand_size:
                        client_data.selected_index -= 2
                elif event.right:
                    if client_data.selected_index < self.hand_size - 2:
                        client_data.selected_index += 2
                elif event.down:
                    if self.step == 1 and client_data.selected_index == self.hand_size:
                        client_data.selected_index = 0
                    elif client_data.selected_index % 2 == 0 and client_data.selected_index < self.hand_size:
                        client_data.selected_index += 1
                elif event.up:
                    if client_data.selected_index % 2 == 0:
                        client_data.selected_index = self.hand_size
                    elif client_data.selected_index % 2 == 1 and client_data.selected_index > 0:
                        client_data.selected_index -= 1

        # draw the players hand
        for i in range(len(hand)):
            y = WIN_HEIGHT - (CARD_HEIGHT * 2) - 30 - CARD_SPACING if i % 2 == 0 else WIN_HEIGHT - CARD_HEIGHT - 30
            c = hand[i]
            x = i // 2 * mult + offset
            selected = False
            if self.turn == p and (self.step == 1 or self.step == 2):
                if card_selected(x, y, event.mouse_pos):
                    client_data.selected_index = i
                    selected = True
                    if event.click or event.enter:
                        if self.step == 1:
                            if network.send_command_to_server(DiscardCommand(p, c)):
                                client_data.selected_index = 0
                        elif self.step == 2:
                            if network.send_command_to_server(FlipCardCommand(p, c)):
                                client_data.selected_index = 0
                elif client_data.selected_index == i:
                    selected = True
                    if event.enter:
                        if self.step == 1:
                            if network.send_command_to_server(DiscardCommand(p, c)):
                                client_data.selected_index = 0
                        elif self.step == 2:
                            if network.send_command_to_server(FlipCardCommand(p, c)):
                                client_data.selected_index = 0
            if c.face_up:
                c.draw(win, resources, x, y, selected=selected and select_frame)
            else:
                resources.draw_card_back(win, client_data.settings.card_back, x, y, frame_count, selected=selected and select_frame)

        # draw opponents hand
        for i in range(len(opponents_hand)):
            y = 30 if i % 2 == 1 else 30 + CARD_HEIGHT + CARD_SPACING
            c = opponents_hand[i]
            x = i // 2 * mult + offset
            if c.face_up:
                c.draw(win, resources, x, y)
            else:
                resources.draw_card_back(win, client_data.settings.card_back, x, y, frame_count)

        # draw the drawn card
        x = WIN_WIDTH - offset // 2 - CARD_WIDTH // 2
        if self.turn == p and self.step == 1:
            self.drawn_card.draw(win, resources, x, WIN_HEIGHT - (CARD_HEIGHT * 3/2) - 30 - CARD_SPACING // 2)
        elif self.turn != p and self.step == 1:
            resources.draw_card_back(win, client_data.settings.card_back, x, 30 + (CARD_HEIGHT * 3/2) + CARD_SPACING // 2, frame_count)

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
                        if network.send_command_to_server(DrawFromDeckCommand(p)):
                            client_data.selected_index = 0
                elif client_data.selected_index == 0:
                    selected = True
                    if event.enter:
                        if network.send_command_to_server(DrawFromDeckCommand(p)):
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
                        if network.send_command_to_server(DrawFromDiscardCommand(p)):
                            client_data.selected_index = self.hand_size
                elif client_data.selected_index == 1:
                    selected = True
                    if event.enter:
                        if network.send_command_to_server(DrawFromDiscardCommand(p)):
                            client_data.selected_index = self.hand_size
            elif self.turn == p and self.step == 1:
                if card_selected(x, y, event.mouse_pos):
                    client_data.selected_index = self.hand_size
                    selected = True
                    if event.click or event.enter:
                        if network.send_command_to_server(DiscardCommand(p, self.drawn_card)):
                            client_data.selected_index = 0
                elif client_data.selected_index == self.hand_size:
                    selected = True
                    if event.enter:
                        if network.send_command_to_server(DiscardCommand(p, self.drawn_card)):
                            client_data.selected_index = 0
            self.top_card.draw(win, resources, x, y, selected=selected and select_frame)
        elif self.top_card is None and self.turn == p and self.step == 1:
            selected = False
            if card_selected(x, y, event.mouse_pos):
                client_data.selected_index = self.hand_size
                selected = True
                if event.click or event.enter:
                    if network.send_command_to_server(DiscardCommand(p, self.drawn_card)):
                        client_data.selected_index = 0
            elif client_data.selected_index == self.hand_size:
                selected = True
                if event.enter:
                    if network.send_command_to_server(DiscardCommand(p, self.drawn_card)):
                        client_data.selected_index = 0
            if selected and select_frame:
                resources.draw_empty_selection(win, x, y)

    def discard_card(self, p, card):
        self.bottom_card = self.top_card
        if card == self.drawn_card:
            self.top_card = self.drawn_card
            self.step = 2
        else:
            self.top_card = card
            self.players[p].play_card(card)
            self.players[p].draw_card(self.drawn_card)
            # TODO check if game over
            self.step = 0
            self.turn = 1 - p
        self.drawn_card = None

    def flip_card(self, p, card):
        self.players[p].flip(card)
        # TODO check if game over
        self.step = 0
        self.turn = 1 - p

    def draw_from_deck(self):
        self.drawn_card = self.deck.deal_card()
        self.step = 1

    def draw_from_discard(self):
        self.drawn_card = self.top_card
        self.top_card = self.bottom_card
        self.step = 1


class DiscardCommand:
    def __init__(self, p, card):
        self.p = p
        self.card = card

    def run(self, game):
        game.discard_card(self.p, self.card)


class FlipCardCommand:
    def __init__(self, p, card):
        self.p = p
        self.card = card

    def run(self, game):
        game.flip_card(self.p, self.card)


class DrawFromDiscardCommand:
    def __init__(self, p):
        self.p = p

    def run(self, game):
        game.draw_from_discard()


class DrawFromDeckCommand:
    def __init__(self, p):
        self.p = p

    def run(self, game):
        game.draw_from_deck()
