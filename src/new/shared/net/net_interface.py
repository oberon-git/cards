import _pickle as pickle


def send_str(sender, data):
    sender.sendall(str.encode(data, encoding='utf-8'))


def recv_str(receiver):
    return receiver.recv(256).decode(encoding='utf-8')


def send_initial_game_data(sender, game, p):
    send_str(sender, str(p))
    data = pickle.dumps(game)
    while data:
        sender.sendall(data[:512])
        data = data[512:]


def recv_initial_game_data(receiver):
    p = int(recv_str(receiver))
    data = []
    while True:
        buff = receiver.recv(512)
        if not buff:
            break
        data.append(buff)
        print(buff)
    data = b''.join(data)
    game = pickle.loads(data)
    return game, p
