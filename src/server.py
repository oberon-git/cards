import socket
from _thread import start_new_thread
from shared import *


file_list = []
for card in Data.CARD_TYPES.values():
    for suit in Data.CARD_SUITS.values():
        file_list.append("assets/cards/" + card + "_of_" + suit + ".png")
for back in Data.CARD_BACKS:
    file_list.append("assets/cards/" + back + ".png")
for i in range(1, 8):
    file_list.append("assets/backgrounds/0" + str(i) + ".png")


class Connection:
    def __init__(self, conn):
        self.conn = conn
        self.ready = False
        self.closed = False

    def close(self):
        self.conn.close()
        self.ready = False
        self.closed = True


def client(conns, game):
    x = 0 if len(conns) == 1 else 1
    y = 0 if len(conns) == 2 else 1
    send_str(conns[x].conn, str(x))
    data = recv_str(conns[x].conn)
    if data == "received":
        send_str(conns[x].conn, str(len(file_list)))
        data = recv_str(conns[x].conn)
        if data == "received":
            for filename in file_list:
                # print("Sending", filename)
                send_str(conns[x].conn, filename)
                data = recv_str(conns[x].conn)
                if data == "send":
                    image = open(filename, 'rb')
                    while True:
                        buff = image.readline(512)
                        if not buff:
                            conns[x].conn.sendall(Data.END)
                            break
                        conns[x].conn.sendall(buff)
                    image.close()
                    # print(filename, "Sent")
                    data = recv_str(conns[x].conn)
                    if data != "received":
                        break
    print("Images Sent")
    connected = False
    while True:
        try:
            if connected:
                if conns[x].closed or conns[y].closed:
                    break
                packet = recv_packet(conns[x].conn)
                map_to_game(packet, game)
                packet = Packet(game)
                send_packet(conns[y].conn, packet)
            if not connected:
                data = conns[x].conn.recv(512)
                if data == Data.END:
                    send_initial_game(conns[x].conn, game)
                    conns[x].ready = True
                else:
                    packet = Packet(game)
                    if len(conns) == 2 and conns[x].ready and conns[y].ready:
                        packet.connected = True
                        send_packet(conns[x].conn, packet)
                        connected = True
                    else:
                        send_packet(conns[x].conn, packet)
        except Exception as e:
            print(e)
            break
    conns[x].close()


def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(Data.ADDR)
            s.listen(2)
            break
        except OSError:
            pass
    print("Listening for Connections")

    connections = []
    game = None
    while True:
        try:
            conn, addr = s.accept()
            connection = Connection(conn)
            if len(connections) == 0:
                connections.append(connection)
                game = Game()
            elif len(connections) == 1:
                if connections[0].closed:
                    connections = [connection]
                    game = Game()
                else:
                    connections.append(connection)
            start_new_thread(client, (connections, game))
            if len(connections) == 2:
                connections = []
        except Exception as e:
            print(e)


main()
