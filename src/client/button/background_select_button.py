from src.shared.shared_data import IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT
from .button import Button


class BackgroundSelectButton(Button):
    def __init__(self, pos, key, action, selected=False, key_triggers=()):
        super().__init__(pos, key, action, selected=selected, key_triggers=key_triggers, args=(key,))
        self.rect = (pos[0], pos[1], IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT)

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

        resources.draw_background_select(win, self.content, self.pos, selected=selected)
