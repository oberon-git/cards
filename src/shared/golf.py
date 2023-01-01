import pygame
from .shared_data import CARD_WIDTH, CARD_HEIGHT, CENTER, BLINK_SPEED, CARD_SPACING, WIN_WIDTH, WIN_HEIGHT
from .shared_data import BLACK, WHITE, FONT_SIZE, FONT_FAMILY, ARROW_SIZE
from .game import Game, card_selected, outline_card


class Golf(Game):
    def __init__(self):
        super().__init__(6)
        self.step = 0

    def draw(self, win, resources, client_data, p, event, frame_count, network):
        super().draw(win, resources, client_data, p, event, frame_count, network)

        select_frame = (frame_count // (BLINK_SPEED * 2)) % 2 == 0
        mult = CARD_WIDTH + CARD_SPACING
        offset = (WIN_WIDTH - (3 * mult) + CARD_SPACING) // 2
        o = 1 - p
        hand = self.players[p].hand()
        opponents_hand = self.players[o].hand()

        '''
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
        '''

        # draw the players hand
        y = WIN_HEIGHT - (CARD_HEIGHT * 2) - 30 - CARD_SPACING
        for i in range(0, len(hand), 2):
            c = hand[i]
            x = i // 2 * mult + offset
            if c.face_up:
                c.draw(win, resources, x, y)
            else:
                resources.draw_card_back(win, client_data.settings.card_back, x, y, frame_count)
        y += CARD_HEIGHT + CARD_SPACING
        for i in range(1, len(hand), 2):
            c = hand[i]
            x = i // 2 * mult + offset
            if c.face_up:
                c.draw(win, resources, x, y)
            else:
                resources.draw_card_back(win, client_data.settings.card_back, x, y, frame_count)

        y = 30
        for i in range(1, len(opponents_hand), 2):
            c = opponents_hand[i]
            x = i // 2 * mult + offset
            if c.face_up:
                c.draw(win, resources, x, y)
            else:
                resources.draw_card_back(win, client_data.settings.card_back, x, y, frame_count)
        y += CARD_HEIGHT + CARD_SPACING
        for i in range(1, len(opponents_hand), 2):
            c = opponents_hand[i]
            x = i // 2 * mult + offset
            if c.face_up:
                c.draw(win, resources, x, y)
            else:
                resources.draw_card_back(win, client_data.settings.card_back, x, y, frame_count)
