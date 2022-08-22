import socket
from _thread import start_new_thread
from random import randint
from shared import *


file_list = []
for card in CARD_TYPES.values():
    for suit in CARD_SUITS.values():
        file_list.append(CARD_ROUTE + card + "_of_" + suit + CARD_EXTENSION)
for back in CARD_BACKS:
    file_list.append(CARD_ROUTE + back + CARD_EXTENSION)
for i in range(1, BACKGROUND_COUNT + 1):
    file_list.append(BACKGROUND_ROUTE + ("0" if i < 10 else "") + str(i) + BACKGROUND_EXTENSION)
for ui_element in UI_ELEMENTS:
    file_list.append(UI_ROUTE + ui_element + UI_EXTENSION)


class Connection:
    def __init__(self, conn):
        self.conn = conn
        self.ready = False
        self.closed = False
        self.reset = False
        self.over = False
        self.hand_sent = False

    def close(self):
        self.conn.close()
        self.ready = False
        self.closed = True

    def start_new_game(self):
        self.reset = False
        self.over = False
        self.hand_sent = False


def send_images(conn):
    send_str(conn, str(len(file_list)))
    data = recv_str(conn)
    if data == "received":
        for filename in file_list:
            send_str(conn, filename)
            data = recv_str(conn)
            if data == "send":
                with open(filename, 'rb') as image:
                    while True:
                        buff = image.readline(512)
                        if not buff:
                            conn.sendall(END)
                            break
                        conn.sendall(buff)
                    data = recv_str(conn)
                    if data != "received":
                        log("Failed To Load Assets")
                        return
    log("Images Sent")


def client(conns, game, p):
    x = 0 if len(conns) == 1 else 1
    y = 0 if len(conns) == 2 else 1
    send_str(conns[x].conn, str(p))
    data = recv_str(conns[x].conn)
    if data == "received":
        send_images(conns[x].conn)
    connected = False
    while True:
        try:
            if connected:
                if conns[x].closed or conns[y].closed:
                    break
                data = recv_packet(conns[x].conn)
                if data == RESET:
                    send_initial_game(conns[x].conn, game)
                    conns[x].start_new_game()
                elif conns[y].reset:
                    send_packet(conns[y].conn, RESET)
                    send_initial_game(conns[y].conn, game)
                    conns[y].start_new_game()
                elif data == GAME_OVER:
                    player = game.get_player(0 if p == 1 else 1)
                    send_player(conns[x].conn, player)
                elif conns[y].over and not conns[y].hand_sent:
                    send_packet(conns[y].conn, GAME_OVER)
                    conns[y].hand_sent = True
                elif type(data) == Player:
                    game.set_player(data, p)
                    send_player(conns[y].conn, game.get_player(p))
                elif type(data) == Packet:
                    if data.reset:
                        game.reshuffle()
                        send_packet(conns[y].conn, RESET)
                        send_initial_game(conns[y].conn, game)
                        conns[x].reset = True
                        conns[y].start_new_game()
                    else:
                        map_to_game(data, game)
                        packet = Packet(game)
                        send_packet(conns[y].conn, packet)
                        if game.over:
                            conns[x].over = True
                            conns[y].over = True
                elif data is None:
                    send_packet(conns[y].conn, None)
            elif not connected:
                data = recv_packet(conns[x].conn)
                if data == NEW_GAME:
                    send_initial_game(conns[x].conn, game)
                    conns[x].ready = True
                else:
                    packet = Packet(game)
                    if len(conns) == 2 and conns[x].ready and conns[y].ready:
                        connected = packet.connected = True
                    send_packet(conns[x].conn, packet)
            tick()
        except Exception as e:
            log(e)
            break
    if len(conns) == 2 and not conns[y].closed:
        packet = Packet(game)
        packet.disconnected = True
        send_packet(conns[y].conn, packet)
    conns[x].close()


def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(ADDR)
            s.listen(2)
            break
        except OSError:
            pass
    log("Listening for Connections", True)

    connections = []
    games = []
    g = 0
    p = 0
    while True:
        try:
            conn, addr = s.accept()
            log("Connected to " + addr[0], True)
            connection = Connection(conn)
            if len(connections) == 0:
                connections.append(connection)
                games.append(Game())
                p = randint(0, 1)
            elif len(connections) == 1:
                if connections[0].closed:
                    connections = [connection]
                    games[g] = Game()
                    p = randint(0, 1)
                else:
                    connections.append(connection)
                    p = 0 if p == 1 else 1
            start_new_thread(client, (connections, games[g], p))
            if len(connections) == 2:
                connections = []
                g += 1
        except Exception as e:
            log(e)


main()
