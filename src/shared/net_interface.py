import pickle


def send_str(conn, s):
    conn.sendall(str.encode(s))


def recv_str(conn):
    s = conn.recv(256)
    return s.decode()


def send_initial_game_data(conn, game, p):
    send_str(conn, str(p))
    recv_str(conn)
    send_game(conn, game)


def recv_initial_game_data(conn):
    p = int(recv_str(conn))
    send_str(conn, "RECEIVED")
    game = recv_game(conn)
    return p, game


def recv_game(conn):
    data = []
    while True:
        buff = conn.recv(512)
        if buff.endswith(b'\n'):
            data.append(buff[:-1])
            break
        data.append(buff)
    data = b''.join(data)
    return pickle.loads(data)


def send_game(conn, game):
    data = pickle.dumps(game)
    while data:
        conn.sendall(data[:512])
        data = data[512:]
    conn.sendall(b'\n')


def send_packet(conn, packet):
    data = pickle.dumps(packet)
    conn.sendall(data)


def recv_packet(conn):
    packet = pickle.loads(conn.recv(2048*64))
    return packet
