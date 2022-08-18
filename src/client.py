import socket
import os
from shared import *


class UserSettings:
    def __init__(self):
        with open("../usersettings.yml", 'r') as user_file:
            self.settings = yaml.safe_load(user_file)
        self.background = self.settings["background"]

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
            print("Trying To Connect To", HOST)
            self.client.connect(ADDR)
            p = int(recv_str(self.client))
            send_str(self.client, "received")
            print("Connected")
            card_list = []
            n = int(recv_str(self.client))
            send_str(self.client, "received")
            if not os.path.exists("assets"):
                os.mkdir("assets")
            if not os.path.exists("assets/cards"):
                os.mkdir("assets/cards")
            if not os.path.exists("assets/backgrounds"):
                os.mkdir("assets/backgrounds")
            for _ in range(n):
                filename = self.client.recv(128).decode()
                card_list.append(filename)
                if not os.path.exists(filename):
                    send_str(self.client, "send")
                    # print("Receiving", filename)
                    with open(filename, 'wb') as file:
                        data = self.recv_image()
                        file.write(data)
                    # print(filename, "Received")
                    send_str(self.client, "received")
                else:
                    send_str(self.client, "skip")
            print("Images Received")
            return p, card_list
        except Exception as e:
            print(e)

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
            print(e)
            return False

    def send(self, game):
        try:
            if game is None:
                self.client.sendall(END)
                return recv_initial_game(self.client)
            elif game.update:
                game.update = False
                packet = Packet(game)
                send_packet(self.client, packet)
            else:
                send_packet(self.client, None)
            packet = recv_packet(self.client)
            if packet == 0:
                return recv_initial_game(self.client), True
            elif packet.disconnected:
                return None, False
            else:
                map_to_game(packet, game)
                return game, False
        except Exception as e:
            print(e)
            return None, False


class Menu:
    def __init__(self, settings):
        self.settings = settings
        self.n = 2
        self.play_button = Button(self.get_button_rect(1), "Play", self.play)
        self.background_select_button = Button(self.get_button_rect(2), "Select Background", self.select_background_action)
        self.back_button = Button((50, WIN_HEIGHT - BUTTON_HEIGHT - 50), "Back", self.back)
        self.background_selects = {}
        self.selected_background = None
        self.start = False
        self.screen = 0

    def get_button_rect(self, x):
        offset = -75 * (self.n - x)
        return WIN_WIDTH // 2 - BUTTON_WIDTH // 2, WIN_HEIGHT // 2 + offset - BUTTON_HEIGHT // 2

    def draw(self, win, resources, clicked, mouse_pos):
        win.fill(WHITE)
        if self.screen == 0:
            self.play_button.draw(win, mouse_pos, clicked, resources)
            self.background_select_button.draw(win, mouse_pos, clicked, resources)
        elif self.screen == 1:
            for key, select in self.background_selects.items():
                select.draw(win, mouse_pos, clicked, resources)
        if self.screen != 0:
            self.back_button.draw(win, mouse_pos, clicked, resources)

    def select_background_action(self):
        self.screen = 1
        images_per_row = 4
        spacing = (WIN_WIDTH - images_per_row * IMAGE_BUTTON_WIDTH) // (images_per_row + 1)
        col_offset = IMAGE_BUTTON_WIDTH + spacing
        row_offset = IMAGE_BUTTON_HEIGHT + spacing
        pos = (spacing, spacing)
        col = 0
        print(BACKGROUND_COUNT)
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
        self.screen = 0

    def play(self):
        self.start = True


def waiting(win, x):
    win.fill(WHITE)
    font = pygame.font.SysFont("Times", 30)
    rect = font.render("Waiting For Opponent.", True, BLACK).get_rect()
    rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
    text = font.render("Waiting For Opponent" + "." * x, True, BLACK)
    win.blit(text, rect)


def event_loop():
    active = True
    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
    return active, clicked, pygame.mouse.get_pos()


def main(win, resources, usersettings, n, p):
    game = n.send(None)
    clock = pygame.time.Clock()

    count = 0
    connected = False
    active = True
    while active:
        try:
            active, clicked, pos = event_loop()
            if connected:
                game.draw(win, resources, usersettings, p, pos, clicked, count)
                game, reset = n.send(game)
                if game is None:
                    return startup()
                if reset:
                    p = 0 if p == 1 else 1
            else:
                connected = n.wait()
                waiting(win, ((count // 24) % 3) + 1)
            count += 1
            clock.tick(FPS)
            pygame.display.update()
        except pygame.error or socket.error:
            break
    pygame.quit()


def draw_menu(win, resources, usersettings, n, p):
    clock = pygame.time.Clock()
    menu = Menu(usersettings)

    active = True
    while active:
        active, clicked, pos = event_loop()
        menu.draw(win, resources, clicked, pos)
        if menu.start:
            return main(win, resources, usersettings, n, p)
        n.wait()
        clock.tick(FPS)
        pygame.display.update()
    pygame.quit()


def startup():
    n = Network()
    p, card_list = n.connect()
    resources = Resources(card_list)
    usersettings = UserSettings()
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    draw_menu(win, resources, usersettings, n, p)


startup()
