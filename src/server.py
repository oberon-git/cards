import socket
from threading import Thread
from random import randint
from shared.shared_data import *
from shared.net import *
from shared.packet import Packet


def client_handler(conn1, conn2, game, p):
    send_initial_game(conn1, game, p)
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

    print('Listening for Connections')
    while True:
        try:
            conn1, addr = s.accept()
            print('Connected to ' + addr[0])
            send_str(conn1, 'WAITING')
            conn2, addr = s.accept()
            print('Connected to ' + addr[0])

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


if __name__ == '__main__':
    new_main()
