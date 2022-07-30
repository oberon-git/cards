from card import Card
from hand import Hand


def print_hand(hand):
    print("[", end="")
    for c in range(len(hand)):
        print(hand[c], end=", " if c < len(hand) - 1 else "")
    print("]")


def main():
    hand = Hand([Card(7, 4), Card(7, 2), Card(3, 1), Card(4, 1), Card(5, 1), Card(6, 1), Card(2, 1)])
    print(hand.is_winning_hand())


main()
