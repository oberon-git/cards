import pickle
from .game import Game


def send_int(conn, i):
    b = str.encode(str(i))
    conn.sendall(b)


def recv_int(conn):
    b = conn.recv(2)
    print(b)
    return int(b.decode())


def send_str(conn, s):
    conn.sendall(str.encode(s))


def recv_str(conn):
    s = conn.recv(256)
    return s.decode()


def send_initial_game(conn, game, p):
    send_packet(conn, {'p': p, 'deck': game.deck, 'players': game.players})


def recv_initial_game(conn):
    game_dict = recv_packet(conn)
    return game_dict['p'], Game(game_dict['deck'], game_dict['players'])


def send_game(conn, game):
    data = pickle.dumps(game)
    conn.sendall(data)


def recv_game(conn):
    data = conn.recv(2048*16)
    return pickle.loads(data)


def send_packet(conn, packet):
    data = pickle.dumps(packet)
    conn.sendall(data)


def recv_packet(conn):
    packet = pickle.loads(conn.recv(2048*4))
    return packet
