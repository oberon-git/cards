from src.shared.shared_data import CARD_WIDTH, CARD_HEIGHT
from .button import Button


class CardSelectButton(Button):
    def __init__(self, pos, key, action, selected=False, key_triggers=()):
        super().__init__(pos, key, action, selected=selected, key_triggers=key_triggers, args=(key,))
        self.rect = (pos[0], pos[1], CARD_WIDTH, CARD_HEIGHT)

    def draw(self, win, resources, event, frame_count):
        selected = False
        if self.in_range(event.mouse_pos):
            selected = True
            if event.click or event.enter:
                self.click()
        elif self.selected:
            selected = True
            if event.enter:
                self.click()

        resources.draw_card_back(win, self.content, self.pos[0], self.pos[1], frame_count, selected=selected)
