import socket
import pickle
from _thread import start_new_thread
from data import Data
from game import Game
from packet import *

file_list = []
for card in Data.CARD_TYPES.values():
    for suit in Data.CARD_SUITS.values():
        file_list.append("assets/cards/" + card + "_of_" + suit + ".png")
for back in Data.CARD_BACKS:
    file_list.append("assets/cards/" + back + ".png")
for x in range(1, 8):
    file_list.append("assets/backgrounds/0" + str(x) + ".png")


count = 0
connections = []
games = {}


def client(g, c, o):
    global connections, games
    p = c % 2
    connections[c][0].send(str.encode(str(p)))
    data = connections[c][0].recv(512).decode()
    if data == "received":
        connections[c][0].send(str.encode(str(len(file_list))))
        data = connections[c][0].recv(512).decode()
        if data == "received":
            for filename in file_list:
                # print("Sending", filename)
                connections[c][0].send(str.encode(filename))
                data = connections[c][0].recv(512).decode()
                if data == "send":
                    image = open(filename, 'rb')
                    while True:
                        buff = image.readline(2048)
                        if not buff:
                            connections[c][0].sendall(Data.END)
                            break
                        connections[c][0].sendall(buff)
                    image.close()
                    # print(filename, "Sent")
                    data = connections[c][0].recv(512).decode()
                    if data != "received":
                        break
    print("Images Sent")
    while True:
        try:
            data = pickle.loads(connections[c][0].recv(1024))
            if data is None:
                connections[c][0].sendall(pickle.dumps(games[g]))
                connections[c][1] = True
            elif games[g].connected():
                if games[g].game.turn == p:
                    map_to_game(data, games[g])
                    packet = Packet(games[g])
                    connections[o][0].sendall(pickle.dumps(packet))
                else:
                    if data.turn != games[g].game.turn:
                        map_to_game(data, games[g])
                        packet = Packet(games[g])
                        connections[o][0].sendall(pickle.dumps(packet))
                    else:
                        connections[o][0].sendall(pickle.dumps(None))
            else:
                connections[p][0].sendall(pickle.dumps(Packet(games[g])))
            if not games[g].connected() and o < len(connections) and connections[c][1] and connections[o][1]:
                games[g].connect()
                packet = Packet(games[g])
                connections[c][0].sendall(pickle.dumps(packet))
                connections[o][0].sendall(pickle.dumps(packet))
        except:
            break
    if games[g] is not None and o < len(connections):
        try:
            connections[o][0].send(pickle.dumps(0))
        except OSError:
            pass
    games[g] = None
    connections[c][0].close()


def main():
    global count
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(Data.ADDR)
    s.listen(5)
    print("Listening For Connections...")

    while True:
        conn, addr = s.accept()
        connections.append([conn, False])
        game_id = count // 2
        if count % 2 == 0:
            games[game_id] = Game('rummy')
            start_new_thread(client, (game_id, len(connections)-1, len(connections)))
        else:
            if game_id not in games:
                count -= 1
                game_id = count // 2
                games[game_id] = Game("rummy")
                start_new_thread(client, (game_id, len(connections)-1, len(connections)))
            else:
                start_new_thread(client, (game_id, len(connections)-1, len(connections)-2))
        count += 1


main()
