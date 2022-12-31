import socket
from threading import Thread
from random import randint
from shared.shared_data import *
from shared.net_interface import *
from shared.rummy import Rummy


def client_handler(conn1, conn2, game, p):
    send_initial_game_data(conn1, game, p)
    while True:
        try:
            command = recv_packet(conn1)
            command.run(game)
            send_game(conn1, game)
            send_game(conn2, game)
        except Exception as e:
            print(e)
            break
    conn1.close()


def is_connected(conn):
    try:
        send_str(conn, 'ping')
        return True
    except:
        return False


def new_main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen(2)

    print('Listening for Connections')

    connected = {}
    while True:
        try:
            conn, addr = s.accept()
            print('Connected to ' + addr[0])
            game_type = recv_str(conn)

            if game_type == 'GOLF':
                print('NO SUPPORT FOR GOLF  YET')
                game_type = 'RUMMY'

            if game_type not in connected:
                connected[game_type] = []
            connected[game_type].append(conn)

            '''
            conns_to_remove = set()
            for conn in connected[game_type]:
                if not is_connected(conn):
                    conns_to_remove.add(conn)
            for conn in conns_to_remove:
                connected[game_type].remove(conn)
            '''

            if len(connected[game_type]) >= 2:
                conn1 = connected[game_type].pop(0)
                conn2 = connected[game_type].pop(0)

                send_str(conn1, 'CONNECTED')
                send_str(conn2, 'CONNECTED')

                p1 = randint(0, 1)
                p2 = 1 - p1

                if game_type == 'RUMMY':
                    game = Rummy()
                else:
                    game = None

                client_thread1 = Thread(target=client_handler, args=(conn1, conn2, game, p1))
                client_thread2 = Thread(target=client_handler, args=(conn2, conn1, game, p2))
                client_thread1.start()
                client_thread2.start()

            else:
                send_str(conn, 'WAITING')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    new_main()
