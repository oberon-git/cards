import pickle


def send_str(conn, s):
    conn.sendall(str.encode(s))


def recv_str(conn):
    s = conn.recv(256)
    return s.decode()


def send_initial_game_data(conn, game, p):
    send_str(conn, str(p))
    recv_str(conn)
    send_game_data(conn, game)


def recv_initial_game_data(conn):
    p = int(recv_str(conn))
    send_str(conn, "RECEIVED")
    game = recv_game_data(conn)
    return p, game


def recv_game_data(conn):
    data = []
    while True:
        buff = conn.recv(512)
        if buff.endswith(b'\n'):
            data.append(buff[:-1])
            break
        data.append(buff)
    data = b''.join(data)
    return pickle.loads(data)


def send_game_data(conn, game_data):
    data = pickle.dumps(game_data)
    while data:
        conn.sendall(data[:512])
        data = data[512:]
    conn.sendall(b'\n')


def send_command(conn, command):
    data = pickle.dumps(command)
    conn.sendall(data)


def recv_command(conn):
    command = pickle.loads(conn.recv(2048))
    return command
