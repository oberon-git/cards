import socket
import os
from shared import *


class UserSettings:
    def __init__(self):
        with open("../usersettings.yml", 'r') as user_file:
            self.settings = yaml.safe_load(user_file)
        self.background = self.settings["background"]
        self.game = self.settings["game"]

    def get_game_name(self):
        return GAMES[self.game]

    def update_background(self, background):
        self.settings["background"] = background
        self.update()
        self.background = self.settings["background"]

    def update(self):
        with open("../usersettings.yml", 'w') as user_file:
            yaml.dump(self.settings, user_file)
        with open("../usersettings.yml", 'r') as user_file:
            self.settings = yaml.safe_load(user_file)


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            log("Trying To Connect To " + HOST)
            self.client.connect(ADDR)
            p = int(recv_str(self.client))
            send_str(self.client, "received")
            log("Connected")
            card_list = []
            n = int(recv_str(self.client))
            send_str(self.client, "received")
            for _ in range(n):
                filename = self.client.recv(128).decode()
                card_list.append(filename)
                if not os.path.exists(filename):
                    send_str(self.client, "send")
                    log("Receiving " + filename)
                    with open(filename, 'wb') as file:
                        data = self.recv_image()
                        file.write(data)
                    log(filename + " Received")
                    send_str(self.client, "received")
                else:
                    send_str(self.client, "skip")
            log("Images Received")
            return p, card_list
        except Exception as e:
            log(e)

    def recv_image(self):
        data = b''
        while True:
            buff = self.client.recv(512)
            if not buff:
                return data
            data += buff
            if data.endswith(END):
                return data[:data.find(END)]

    def wait(self):
        try:
            send_packet(self.client, None)
            packet = recv_packet(self.client)
            return packet.connected
        except Exception as e:
            log(e)
            return False

    def send(self, game, p, skip_send=False):
        try:
            if not skip_send:
                if game is None:
                    send_packet(self.client, NEW_GAME)
                    return recv_initial_game(self.client)
                elif game.update:
                    game.update = False
                    packet = Packet(game)
                    send_packet(self.client, packet)
                else:
                    send_packet(self.client, None)
            packet = recv_packet(self.client)
            if packet == RESET:
                return recv_initial_game(self.client), True
            elif packet == GAME_OVER:
                send_packet(self.client, game.get_player(p))
                self.send(game, p, True)
            elif type(packet) == Player:
                game.set_opponent(packet, p)
            elif type(packet) == Packet:
                if packet.disconnected:
                    return None, False
                else:
                    map_to_game(packet, game)
            return game, False
        except Exception as e:
            log(e)
            return None, False


class Resources:
    def __init__(self, file_list):
        self.cards = {}
        self.backgrounds = {}
        self.ui = {}
        for filename in file_list:
            if "cards" in filename:
                key = filename.replace("assets/cards/", "").replace("_of_", "").replace(".png", "")
                self.cards[key] = pygame.image.load(filename)
            elif "backgrounds" in filename:
                key = int(filename.replace("assets/backgrounds/", "").replace(".png", ""))
                self.backgrounds[key] = pygame.image.load(filename)
            elif "ui" in filename:
                if "icon" in filename:
                    self.icon = pygame.image.load(filename)
                if "arrow" in filename:
                    self.arrow = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(filename), (ARROW_SIZE, ARROW_SIZE)), 90)

    def draw_card(self, win, key, x, y):
        image = self.cards[key]
        win.blit(image, (x, y))

    def draw_background(self, win, key):
        image = pygame.transform.scale(self.backgrounds[key], (WIN_WIDTH, WIN_HEIGHT))
        win.blit(image, (0, 0))

    def draw_background_select(self, win, key, pos):
        image = pygame.transform.scale(self.backgrounds[key], (IMAGE_BUTTON_WIDTH, IMAGE_BUTTON_HEIGHT))
        win.blit(image, pos)

    def draw_arrow(self, win, pos, orientation):
        image = pygame.transform.rotate(self.arrow, 180 if orientation == 0 else 0)
        win.blit(image, pos)


class Menu:
    def __init__(self, settings, paused=False):
        self.settings = settings
        self.paused = paused
        self.n = 2
        self.play_button = Button(self.get_button_rect(1), "Continue" if self.paused else "Play", self.play)
        self.background_select_button = Button(self.get_button_rect(2), "Select Background", self.select_background_action)
        self.back_button = Button((50, WIN_HEIGHT - BUTTON_HEIGHT - 50), "Back", self.back)
        self.pause_button = Button((WIN_WIDTH - 50, 20), None, self.pause)
        self.background_selects = {}
        self.selected_background = None
        self.start = self.active = False
        self.screen = 2 if self.paused else 0

    def get_button_rect(self, x):
        offset = -75 * (self.n - x)
        return CENTER[0] - BUTTON_WIDTH // 2, CENTER[1] + offset - BUTTON_HEIGHT // 2

    def draw(self, win, resources, clicked, mouse_pos):
        if self.screen != 2:
            resources.draw_background(win, self.settings.background)
        if self.screen == 0:
            self.play_button.draw(win, mouse_pos, clicked, resources)
            self.background_select_button.draw(win, mouse_pos, clicked, resources)
        elif self.screen == 1:
            for key, select in self.background_selects.items():
                select.draw(win, mouse_pos, clicked, resources)
            self.back_button.draw(win, mouse_pos, clicked, resources)
        elif self.screen == 2:
            self.pause_button.draw(win, mouse_pos, clicked, resources)
        elif self.screen == 3:
            self.play_button.draw(win, mouse_pos, clicked, resources)
            self.background_select_button.draw(win, mouse_pos, clicked, resources)

    def pause(self):
        self.screen = 3
        self.active = True

    def select_background_action(self):
        self.screen = 1
        images_per_row = 4
        spacing = (WIN_WIDTH - images_per_row * IMAGE_BUTTON_WIDTH) // (images_per_row + 1)
        col_offset = IMAGE_BUTTON_WIDTH + spacing
        row_offset = IMAGE_BUTTON_HEIGHT + spacing
        pos = (spacing, spacing)
        col = 0
        log(BACKGROUND_COUNT)
        for i in range(1, BACKGROUND_COUNT + 1):
            selected = i == self.settings.background
            self.background_selects[i] = (Button(pos, i, self.select_background, selected))
            col += 1
            if col == 4:
                col = 0
                pos = (spacing, pos[1] + row_offset)
            else:
                pos = (pos[0] + col_offset, pos[1])

    def select_background(self, key):
        self.background_selects[self.settings.background].selected = False
        self.settings.update_background(key)
        self.background_selects[key].selected = True

    def back(self):
        self.screen = 3 if self.paused else 0

    def play(self):
        self.start = True
        if self.paused:
            self.active = False
            self.screen = 2

    def escape(self, escaped):
        if escaped:
            if self.screen == 0:
                return False
            elif self.screen == 1:
                self.back()
            elif self.screen == 2:
                self.pause()
            elif self.screen == 3:
                self.play()
        return True


def waiting(win, x):
    win.fill(WHITE)
    rect = FONT.render("Waiting For Opponent.", True, BLACK).get_rect()
    rect.center = CENTER
    text = FONT.render("Waiting For Opponent." + "." * x, True, BLACK)
    win.blit(text, rect)


def event_loop():
    active = True
    clicked = escaped = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                escaped = True
    return active, clicked, escaped, pygame.mouse.get_pos()


def main(win, resources, usersettings, n, p):
    game = n.send(None, p)
    menu = None

    count = 0
    connected = False
    active = True
    while active:
        try:
            active, clicked, escaped, pos = event_loop()
            if connected:
                menu.escape(escaped)
                if not menu.active:
                    game.draw(win, resources, usersettings, p, pos, clicked, count)
                menu.draw(win, resources, clicked, pos)
                game, reset = n.send(game, p)
                if game is None:
                    return startup()
                if reset:
                    p = 0 if p == 1 else 1
            else:
                connected = n.wait()
                waiting(win, ((count // BLINK_SPEED) % 3))
                if connected:
                    menu = Menu(usersettings, True)
            count += 1
            tick()
            pygame.display.update()
        except pygame.error or socket.error:
            break


def draw_menu(win, resources, usersettings, n, p):
    menu = Menu(usersettings)

    active = True
    while active:
        active, clicked, escaped, pos = event_loop()
        if active:
            active = menu.escape(escaped)
        menu.draw(win, resources, clicked, pos)
        if menu.start:
            return main(win, resources, usersettings, n, p)
        n.wait()
        tick()
        pygame.display.update()


def setup_win(settings, resources):
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(settings.get_game_name())
    pygame.display.set_icon(resources.icon)
    return win


def setup_dir():
    if not os.path.exists("assets"):
        os.mkdir("assets")
    if not os.path.exists("assets/cards"):
        os.mkdir("assets/cards")
    if not os.path.exists("assets/backgrounds"):
        os.mkdir("assets/backgrounds")
    if not os.path.exists("assets/ui"):
        os.mkdir("assets/ui")
    if not os.path.exists("../usersettings.yml"):
        default_settings = {"background": 1, "game": 1}
        with open("../usersettings.yml", 'w') as user_file:
            yaml.dump(default_settings, user_file)


def startup():
    setup_dir()
    n = Network()
    p, card_list = n.connect()
    resources = Resources(card_list)
    usersettings = UserSettings()
    win = setup_win(usersettings, resources)
    draw_menu(win, resources, usersettings, n, p)


if __name__ == "__main__":
    startup()
    pygame.quit()
