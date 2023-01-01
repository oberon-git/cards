import socket
from threading import Thread
from src.shared.net_interface import send_str, recv_str, send_command, recv_initial_game_data, recv_game
from src.shared.shared_data import ADDR


class Network:
    def __init__(self, game_type):
        self.game_type = game_type.upper()

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.connected = False
        connection_handler = Thread(target=self.connect)
        connection_handler.start()

        self.game = self.p = None
        self.game_started = False
        self.kill_all_threads = False

    def connect(self):
        try:
            send_str(self.client, self.game_type)
            data = recv_str(self.client)
            while data != 'CONNECTED':
                data = recv_str(self.client)
            self.connected = True
        except Exception as e:
            print(e)

    def start_game(self):
        self.p, self.game = recv_initial_game_data(self.client)
        self.game_started = True
        receiver = Thread(target=self.recv_packets_from_server)
        receiver.daemon = True
        receiver.start()

    def recv_packets_from_server(self):
        while True:
            try:
                if self.kill_all_threads:
                    return
                self.game = recv_game(self.client)
            except Exception as e:
                print(e)

    def send_command_to_server(self, command):
        send_command(self.client, command)

    def update(self, win, resources, client_data, input_event, frame_count):
        self.game.draw(win, resources, client_data, self.p, input_event, frame_count, self)

    def close(self):
        self.kill_all_threads = True
        self.client.close()
