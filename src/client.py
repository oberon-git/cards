import socket
import os
from shared import *


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            print("Trying To Connect To", Data.HOST)
            self.client.connect(Data.ADDR)
            p = int(recv_str(self.client))
            send_str(self.client, "received")
            print("Connected")
            card_list = []
            n = int(recv_str(self.client))
            send_str(self.client, "received")
            # print(f"Sending {n} Images")
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
                    send_str(self.client, "received")
                    # print(filename, "Received")
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
            if data.endswith(Data.END):
                return data[:data.find(Data.END)]

    def wait(self, game):
        try:
            send_packet(self.client, Packet(game))
            packet = recv_packet(self.client)
            return packet.connected
        except Exception as e:
            print(e)
            return False

    def send(self, game):
        try:
            if game is None:
                self.client.sendall(Data.END)
                return recv_initial_game(self.client)
            packet = Packet(game)
            send_packet(self.client, packet)
            packet = recv_packet(self.client)
            map_to_game(packet, game)
            return game
        except Exception as e:
            print(e)
            return None


def waiting(win, x):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont("Times", 30)
    rect = font.render("Waiting For Opponent", True, (0, 0, 0)).get_rect()
    rect.center = (win.get_width() // 2, win.get_height() // 2)
    text = font.render("Waiting For Opponent" + "." * x, True, (0, 0, 0))
    win.blit(text, rect)


def main():
    n = Network()
    p, card_list = n.connect()
    game = n.send(None)
    resources = Resources(card_list)

    pygame.init()
    win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    count = 0
    active = True
    connected = False
    while active:
        try:
            clicked = False
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    pygame.quit()
                # if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                #    win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                    pos = pygame.mouse.get_pos()
            if connected:
                game = n.send(game)
                game.draw(win, resources, p, pos, clicked)
            else:
                connected = n.wait(game)
                waiting(win, ((count // 24) % 3) + 1)
            count += 1
            clock.tick(60)
            pygame.display.update()
            if game is None:
                active = False
                pygame.quit()
        except Exception as e:
            print(e)
            active = False
            pygame.quit()


main()