import socket
from threading import Thread
from random import randint
from shared.shared_data import *
from shared.net import *
from shared.player import Player
from shared.packet import Packet
from shared.packet import map_to_game
from server.connection import Connection


def client(conns, game, p):
    x = 0 if len(conns) == 1 else 1
    y = 0 if len(conns) == 2 else 1
    send_str(conns[x].conn, str(p))
    data = recv_str(conns[x].conn)
    if data != "received":
        return
    connected = False
    while True:
        try:
            if connected:
                if conns[x].closed or conns[y].closed:
                    break
                data = recv_packet(conns[x].conn)
                if data == RESET:
                    send_packet(conns[y].conn, None)
                    send_initial_game(conns[x].conn, game)
                    conns[x].start_new_game()
                elif conns[y].reset:
                    send_packet(conns[y].conn, RESET)
                elif conns[y].over:
                    send_packet(conns[y].conn, GAME_OVER)
                    conns[y].over = False
                elif type(data) == Player:
                    game.set_player(data, p)
                    send_packet(conns[y].conn, game.get_player(p))
                elif type(data) == Packet:
                    if data.reset:
                        game.reshuffle()
                        send_packet(conns[y].conn, RESET)
                        send_initial_game(conns[y].conn, game)
                        conns[x].reset = True
                        conns[y].start_new_game()
                    else:
                        over = data.over and not game.over
                        map_to_game(data, game)
                        packet = Packet(game)
                        send_packet(conns[y].conn, packet)
                        if over:
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
        except Exception as e:
            print(e)
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
    print("Listening for Connections")

    connections = []
    games = []
    g = 0
    p = 0
    while True:
        try:
            conn, addr = s.accept()
            print("Connected to " + addr[0])
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
                    p = 1 - p
            client_thread = Thread(target=client, args=(connections.copy(), games[g], p))
            client_thread.start()
            if len(connections) == 2:
                connections = []
                g += 1
        except Exception as e:
            print(e)


def client_handler(conn1, conn2, game, p):
    def send_packets_to_client(conn):
        while True:
            try:
                send_packet(conn, Packet(game))
            except:
                break

    send_initial_game(conn1, game, p)
    # sender = Thread(target=send_packets_to_client, args=(conn2,))
    # sender.start()
    while True:
        try:
            command = recv_packet(conn1)
            command.run(game)
            send_packet(conn1, Packet(game))
            send_packet(conn2, Packet(game))
        except Exception as e:
            print(e)
            break
    conn1.close()


def new_main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen(2)

    while True:
        try:
            conn1, addr = s.accept()
            print("Connected to " + addr[0])
            send_str(conn1, 'WAITING')
            conn2, addr = s.accept()
            print("Connected to " + addr[0])

            send_str(conn1, 'CONNECTED')
            send_str(conn2, 'CONNECTED')

            p1 = randint(0, 1)
            p2 = 1 - p1

            game = Game()

            client_thread1 = Thread(target=client_handler, args=(conn1, conn2, game, p1))
            client_thread2 = Thread(target=client_handler, args=(conn2, conn1, game, p2))
            client_thread1.start()
            client_thread2.start()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    new_main()
