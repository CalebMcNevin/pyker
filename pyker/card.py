from __future__ import annotations
from .enums import Suit, Rank
from typing import Tuple


class Card(object):

    def __init__(self, card_def: str | Tuple[Rank, Suit]):
        match card_def:
            case str():
                self.rank, self.suit = Card.parse_card(card_def)
            case tuple():
                self.rank, self.suit = card_def
            case _:
                raise ValueError

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        if (self.rank == Rank.ACE) ^ (other.rank == Rank.ACE):
            return True
        return self.rank.number < other.rank.number

    def __gt__(self, other):
        if (self.rank == Rank.ACE) ^ (other.rank == Rank.ACE):
            return True
        return self.rank.number > other.rank.number

    def __le__(self, other):
        return (self == other) or (self < other)

    def __ge__(self, other):
        return (self == other) or (self > other)

    def __matmul__(self, other):
        """Returns True if self and other are adjacent"""
        if self == other:
            return False
        if abs(self.rank.number - other.rank.number) == 1:
            return True
        if self.rank == Rank.ACE or other.rank == Rank.ACE:
            if self.rank == Rank.TWO or other.rank == Rank.TWO:
                return True
            if self.rank == Rank.KING or other.rank == Rank.KING:
                return True
        return False

    def __lshift__(self, other):
        if self.rank == Rank.ACE and other.rank == Rank.KING:
            return False
        if self.rank == Rank.TWO and other.rank == Rank.ACE:
            return False
        return self < other and self @ other

    def __rshift__(self, other):
        if self.rank == Rank.ACE and other.rank == Rank.TWO:
            return False
        if self.rank == Rank.KING and other.rank == Rank.ACE:
            return False
        return self > other and self @ other

    def __str__(self):
        return f"{self.rank.alias}{self.suit.symbol}"
    
    @staticmethod
    def parse_card(card_def: str):
        if len(card_def.strip()) != 2:
            raise ValueError(
                'card_def must be two characters long. Ex: \'AD\'')
        enums = list(Rank) + list(Suit)
        mapping = {e.alias: e for e in enums}
        els = [mapping[e] for e in card_def]
        rank = list(filter(lambda e: type(e) == Rank, els))[0]
        suit = list(filter(lambda e: type(e) == Suit, els))[0]
        return (rank, suit)

