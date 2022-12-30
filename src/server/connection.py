class Connection:
    def __init__(self, conn):
        self.conn = conn
        self.ready = False
        self.closed = False
        self.reset = False
        self.over = False
        self.hand_sent = False

    def close(self):
        self.conn.close()
        self.ready = False
        self.closed = True

    def start_new_game(self):
        self.reset = False
        self.over = False
        self.hand_sent = False
