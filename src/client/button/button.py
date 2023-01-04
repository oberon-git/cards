class Button:
    def __init__(self, pos, content, action, selected=False, key_triggers=(), args=(), kwargs=None):
        self.pos = pos
        self.content = content
        self.action = action
        self.selected = selected
        self.key_triggers = key_triggers
        self.args = args
        if kwargs is None:
            self.kwargs = {}

        self.rect = (0, 0, 0, 0)

    def draw(self, win, resources, event, frame_count):
        raise Exception('Cannot call abstract method.')

    def click(self):
        self.action(*self.args, *self.kwargs)

    def in_range(self, pos):
        if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2]:
            if self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
                return True
        return False
