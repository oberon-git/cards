import socket
import threading
from src import net_data
from src import net_interface


class Network:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(net_data.ADDR)
        self.connected = False
        connected_thread = threading.Thread(target=self.connection_handler)
        connected_thread.start()

    def connection_handler(self):
        while True:
            try:
                data = net_interface.recv_str(self.client_socket)
                if data == 'CONNECTED':
                    self.connected = True
                    break
            except:
                break

    def get_initial_game_data(self):
        net_interface.send_str(self.client_socket, 'READY')
        game, p = net_interface.recv_initial_game_data(self.client_socket)
        return game, p


