class Data:
    CARD_TYPES = {1: "ace", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "jack", 12: "queen", 13: "king"}
    CARD_SUITS = {1: "spades", 2: "hearts", 3: "clubs", 4: "diamonds"}
    CARD_BACKS = ("castle_back_01", "castle_back_02")
    CARD_WIDTH = 69
    CARD_HEIGHT = 94
    BACKGROUND_COLOR = (100, 100, 100)
    HOST = '173.230.150.237'
    PORT = 13058
    ADDR = (HOST, PORT)
    END = str.encode("EOF")

