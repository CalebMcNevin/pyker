from __future__ import annotations
from enum import Enum
from functools import total_ordering


class Suit(Enum):
    SPADES = (1, 'Spades', 'S', '♠️')
    HEARTS = (2, 'Hearts', 'H', '♥️')
    CLUBS = (3, 'Clubs', 'C', '♣️')
    DIAMONDS = (4, 'Diamonds', 'D', '♦️')

    def __init__(self, index, long_alias, alias, symbol):
        self.index = index
        self.long_alias = long_alias
        self.alias = alias
        self.symbol = symbol

    def __repr__(self):
        return f'<Rank.{self.name}>'


@total_ordering
class Rank(Enum):
    ACE = (1, 'Ace', 'A')
    TWO = (2, 'Two', '2')
    THREE = (3, 'Three', '3')
    FOUR = (4, 'Four', '4')
    FIVE = (5, 'Five', '5')
    SIX = (6, 'Six', '6')
    SEVEN = (7, 'Seven', '7')
    EIGHT = (8, 'Eight', '8')
    NINE = (9, 'Nine', '9')
    TEN = (10, 'Ten', 'T')
    JACK = (11, 'Jack', 'J')
    QUEEN = (12, 'Queen', 'Q')
    KING = (13, 'King', 'K')

    def __init__(self, number, long_alias, alias):
        self.number = number
        self.long_alias = long_alias
        self.alias = alias

    def __repr__(self):
        return f'<Suit.{self.name}>'

    def __eq__(self, other):
        return self.number == other.number

    def __gt__(self, other):
        if other == Rank.ACE:
            return False
        if self == Rank.ACE:
            return other != Rank.ACE
        return self.number > other.number

    def __lt__(self, other):
        if self == Rank.ACE:
            return False
        if other == Rank.ACE:
            return self != Rank.ACE
        return self.number < other.number


class HandType(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10
