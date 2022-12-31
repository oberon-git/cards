import pickle


def send_str(conn, s):
    conn.sendall(str.encode(s))


def recv_str(conn):
    s = conn.recv(256)
    return s.decode()


def send_initial_game_data(conn, game, p):
    send_packet(conn, {'p': p, 'game': game})


def recv_initial_game_data(conn):
    game_dict = recv_packet(conn)
    return game_dict['p'], game_dict['game']


def recv_game(conn):
    data = conn.recv(2048*16)
    return pickle.loads(data)


def send_game(conn, game):
    data = pickle.dumps(game)
    conn.sendall(data)


def send_packet(conn, packet):
    data = pickle.dumps(packet)
    conn.sendall(data)


def recv_packet(conn):
    packet = pickle.loads(conn.recv(2048*16))
    return packet
