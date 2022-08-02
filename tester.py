from card import Card
from hand import Hand


def print_hand(hand):
    print("[", end="")
    for c in range(len(hand)):
        print(hand[c], end=", " if c < len(hand) - 1 else "")
    print("]")


def main():
    hand = Hand([Card(6, 1), Card(6, 2), Card(7, 2), Card(8, 2), Card(7, 4), Card(10, 2), Card(10, 3)])
    print(hand.is_winning_hand())
    print(hand.h[0].sort)


main()
