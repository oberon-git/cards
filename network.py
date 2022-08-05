import socket
import pickle
import os
from data import Data
from packet import *


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            print("Trying To Connect To", Data.HOST)
            self.client.connect(Data.ADDR)
            p = int(self.client.recv(4).decode())
            self.client.send(str.encode("received"))
            print("Connected")
            card_list = []
            n = int(self.client.recv(4).decode())
            self.client.send(str.encode("received"))
            print(f"Sending {n} Images")
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
                    self.client.send(str.encode("send"))
                    # print("Receiving", filename)
                    with open(filename, 'wb') as file:
                        data = self.recv()
                        file.write(data)
                    self.client.send(str.encode("received"))
                    # print(filename, "Received")
                else:
                    self.client.send(str.encode("skip"))
            print("Images Received")
            return p, card_list
        except socket.error as e:
            print(e)

    def recv(self):
        data = b''
        while True:
            buff = self.client.recv(512)
            if not buff:
                return data
            data += buff
            if data.endswith(Data.END):
                return data[:data.find(Data.END)]

    def send(self, data):
        try:
            if data is None:
                self.client.send(pickle.dumps(data))
                return pickle.loads(self.client.recv(2048*2048*512))
            data_packet = Packet(data)
            self.client.send(pickle.dumps(data_packet))
            server_packet = pickle.loads(self.client.recv(1024))
            if server_packet == 0:
                print("Connection Lost")
                return None
            elif type(server_packet) == Packet:
                map_to_game(server_packet, data)
            return data
        except socket.error as e:
            print(e)
