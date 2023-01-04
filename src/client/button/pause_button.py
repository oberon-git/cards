from .button import Button


class PauseButton(Button):
    def __init__(self, pos, action, selected=False, key_triggers=()):
        super().__init__(pos, None, action, selected=selected, key_triggers=key_triggers)
        self.rect = (self.pos[0], self.pos[1], 30, 40)

    def draw(self, win, resources, event, frame_count):
        clicked = False
        for trigger in self.key_triggers:
            if event.__getattribute__(trigger):
                self.click()
                clicked = True
                break
        if not clicked and self.in_range(event.mouse_pos):
            if event.click or event.enter:
                self.click()

        resources.draw_pause_button(win, self.pos)

