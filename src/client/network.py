import socket
from threading import Thread
from src.shared.net import *
from src.shared.shared_data import *
from src.shared.packet import map_to_game


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.connected = False
        connection_handler = Thread(target=self.connect)
        connection_handler.start()

        self.game = self.p = None
        self.kill_all_threads = False

    def connect(self):
        try:
            data = recv_str(self.client)
            while data != 'CONNECTED':
                if self.kill_all_threads:
                    return
                data = recv_str(self.client)
            self.connected = True
        except Exception as e:
            print(e)

    def start_game(self):
        self.p, self.game = recv_initial_game(self.client)
        receiver = Thread(target=self.recv_packets_from_server)
        receiver.start()

    def recv_packets_from_server(self):
        try:
            while True:
                if self.kill_all_threads:
                    return
                packet = recv_packet(self.client)
                map_to_game(packet, self.game)
        except Exception as e:
            print(e)

    def send_command_to_server(self, command):
        send_packet(self.client, command)

    def update(self, win, resources, usersettings, mouse_pos, clicked, count):
        self.game.draw(win, resources, usersettings, self.p, mouse_pos, clicked, count, self)
