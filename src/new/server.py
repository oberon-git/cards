import socket
import threading
from random import randint
from src.new.shared.net import net_data
from src.new.shared.net import net_interface
from src.new.shared.game.rummy import Rummy


games = {}


def handle_client_connection(conn1, conn2, game_id, p):
    global games

    data = net_interface.recv_str(conn1)
    if data == 'READY':
        net_interface.send_initial_game_data(conn1, games[game_id], p)
    while True:
        try:
            pass
        except:
            break
    conn1.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(net_data.ADDR)
    server_socket.listen(5)

    print('Waiting for connections')

    count = 0
    while True:
        conn1, addr = server_socket.accept()
        print(f'Connected to {addr[0]}')
        net_interface.send_str(conn1, 'WAITING')
        conn2, addr = server_socket.accept()
        print(f'Connected to {addr[0]}')
        net_interface.send_str(conn1, 'CONNECTED')
        net_interface.send_str(conn2, 'CONNECTED')

        p1 = randint(0, 1)
        p2 = 1 - p1
        count += 1
        games[count] = Rummy()

        client_thread1 = threading.Thread(target=handle_client_connection, args=(conn1, conn2, count, p1))
        client_thread2 = threading.Thread(target=handle_client_connection, args=(conn2, conn1, count, p2))
        client_thread1.start()
        client_thread2.start()


if __name__ == '__main__':
    main()
