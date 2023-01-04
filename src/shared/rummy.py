from .shared_data import CARD_WIDTH, CARD_HEIGHT, CENTER, BLINK_SPEED, CARD_SPACING, WIN_WIDTH, WIN_HEIGHT
from .game import Game, card_selected


class Rummy(Game):
    def __init__(self):
        super().__init__(7, face_up=True, sort_hand=True)
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
            selected = new = False
            if self.turn == p and self.step == 1 and not self.over:
                if card_selected(x, y, event.mouse_pos):
                    client_data.selected_index = i
                    selected = True
                    if event.click or event.enter:
                        if network.send_command_to_server(DiscardCommand(p, c)):
                            client_data.selected_index = 0
                elif i == client_data.selected_index:
                    selected = True
                    if event.enter:
                        if network.send_command_to_server(DiscardCommand(p, c)):
                            client_data.selected_index = 0
                elif self.turn == p and self.step == 1 and not self.over and self.new_card_index == i:
                    new = True
            c.draw(win, resources, x, y, selected=selected and select_frame, new=new and select_frame)

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
                        if network.send_command_to_server(DrawFromDeckCommand(p)):
                            client_data.selected_index = 0
                elif client_data.selected_index == 0:
                    selected = True
                    if event.enter and not client_data.command_processing:
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
                            client_data.selected_index = 0
                elif client_data.selected_index == 1:
                    selected = True
                    if event.enter:
                        if network.send_command_to_server(DrawFromDiscardCommand(p)):
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
        if self.won(p):
            self.winner = p
            self.over = True
        self.bottom_card = self.top_card
        self.top_card = c
        self.step = 0
        self.turn = 1 - self.turn

    def won(self, p):
        copy = self.players[p].hand().copy()
        self.players[p].sort_by_suit()
        runs = []
        c = 0
        while c < len(self.players[p].hand()):
            run = set()
            run.add(self.players[p].hand()[c])
            while c < len(self.players[p].hand())-1 and self.players[p].hand()[c].suit() == self.players[p].hand()[c+1].suit() \
                    and (self.players[p].hand()[c].value() == self.players[p].hand()[c+1].value()-1 or self.players[p].hand()[c].value() == 13
                         and self.players[p].hand()[c+1].value() == 1):
                c += 1
                run.add(self.players[p].hand()[c])
                if c < len(self.players[p].hand())-1 and self.players[p].hand()[c].value() == 13 and self.players[p].hand()[c+1].value() == 1:
                    break
            if len(run) >= 3:
                runs.append(run)
            c += 1

        self.players[p].sort_by_value()
        pairs = []
        c = 0
        while c < len(self.players[p].hand()):
            pair = set()
            pair.add(self.players[p].hand()[c])
            while c < len(self.players[p].hand())-1 and self.players[p].hand()[c].value() == self.players[p].hand()[c+1].value():
                c += 1
                pair.add(self.players[p].hand()[c])
            if len(pair) >= 3:
                pairs.append(pair)
            c += 1
        self.players[p].set_hand(copy)

        for i in range(len(runs)-1):
            if len(runs[i]) == 7:
                return True
            for j in range(i+1, len(runs)):
                if len(runs[i]) + len(runs[j]) == 7:
                    return True
        for i in range(len(pairs)-1):
            for j in range(i+1, len(pairs)):
                if len(pairs[i]) + len(pairs[j]) == 7:
                    return True
        for pair in pairs:
            for run in runs:
                points = len(run)
                for card in pair:
                    if card in run:
                        points -= 1
                if points + len(pair) == 7:
                    return True
        return False


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
