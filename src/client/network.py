import socket
from threading import Thread
from src.shared.net import *
from src.shared.shared_data import *
from src.shared.packet import map_to_game
from src.shared.packet import Packet
from src.shared.player import Player


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.connected = False
        connection_handler = Thread(target=self.connect)
        connection_handler.start()

        self.game = None
        self.p = -1

    def connect(self):
        try:
            data = recv_str(self.client)
            while data != 'CONNECTED':
                data = recv_str(self.client)
            self.connected = True
        except Exception as e:
            print(e)

    def start_game(self):
        self.p, self.game = recv_initial_game(self.client)
        receiver = Thread(target=self.recv_packets_from_server)
        # sender = Thread(target=self.send_packets_to_server)
        receiver.start()
        # sender.start()

    def recv_packets_from_server(self):
        while True:
            try:
                packet = recv_packet(self.client)
                map_to_game(packet, self.game)
            except:
                break

    def send_command_to_server(self, command):
        send_packet(self.client, command)

    def update(self, win, resources, usersettings, mouse_pos, clicked, count):
        self.game.draw(win, resources, usersettings, self.p, mouse_pos, clicked, count, self)

    def send_packets_to_server(self):
        while True:
            try:
                if self.game.turn == self.p:
                    if self.game.update:
                        self.game.turn = 1 - self.p
                        self.game.update = False
                    data = Packet(self.game)
                    send_packet(self.client, data)
            except:
                pass

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
                send_packet(self.client, RESET)
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
            print(e)
            return None, False
