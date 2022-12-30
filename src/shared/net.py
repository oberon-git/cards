import pickle
from .rummy import Rummy


def send_str(conn, s):
    conn.sendall(str.encode(s))


def recv_str(conn):
    s = conn.recv(256)
    return s.decode()


def send_initial_game(conn, game, p):
    send_packet(conn, {'p': p, 'deck': game.deck, 'players': game.players})


def recv_initial_game(conn):
    game_dict = recv_packet(conn)
    return game_dict['p'], Rummy(game_dict['deck'], game_dict['players'])


def send_packet(conn, packet):
    data = pickle.dumps(packet)
    conn.sendall(data)


def recv_packet(conn):
    packet = pickle.loads(conn.recv(2048*16))
    return packet
