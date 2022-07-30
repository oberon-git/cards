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
                filename = self.client.recv(512).decode()
                card_list.append(filename)
                self.client.send(str.encode("send"))
                # print("Receiving", filename)
                with open(filename, 'wb') as file:
                    buff = self.client.recv(2048)
                    file.write(buff)
                with open(filename, 'ab') as file:
                    while True:
                        buff = self.client.recv(2048)
                        if buff in Data.END or buff == b'' or not buff:
                            break
                        if buff.endswith(Data.END):
                            buff = buff[:buff.find(Data.END)]
                            file.write(buff)
                            break
                        file.write(buff)
                self.client.send(str.encode("received"))
                # print(filename, "Received")
            print("Images Received")
            return p, card_list
        except socket.error as e:
            print(e)

    def send(self, game):
        try:
            if game is None:
                self.client.send(pickle.dumps(game))
                return pickle.loads(self.client.recv(2048*4))
            packet = Packet(game)
            self.client.send(pickle.dumps(packet))
            packet = pickle.loads(self.client.recv(1024))
            if packet == 0:
                print("Connection Lost")
                return None
            elif type(packet) == Packet:
                map_to_game(packet, game)
            return game
        except socket.error as e:
            print(e)
