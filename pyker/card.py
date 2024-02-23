"""Module for representing and managing individual playing cards.

This module defines a `Card` class that represents a single playing card. Each card has a rank
(e.g., Ace, Two, Three, etc.) and a suit (e.g., Hearts, Diamonds, Clubs, Spades). The Card class 
also implements methods for comparison of rank.

Classes:
    Card: Represents a single playing card with a rank and a suit.

Methods:
    __eq__: (==) Compare two cards for equality based on their ranks and suits.
    __lt__: (<)  Compare two cards to determine if one is less than the other based on rank.
    __gt__: (>)  Compare two cards to determine if one is greater than the other based on rank.
    __le__: (<=) Compare two cards to determine if one is less than or equal to the other.
    __ge__: (>=) Compare two cards to determine if one is greater than or equal to the other.
    __matmul__: (@)  Check if two cards are adjacent to each other in rank (ex. 8♦️  @ 7♣️ )
    __lshift__: (<<) Check if left card is directly below right card in rank (ex. K♦️  << A♥️ )
    __rshift__: (>>) Check if left card is directly above right card in rank (ex. A♥️  >> K♦️ )
    __repr__: Return a string representation of the card instance.
    __str__: Return a string representation of the card for printing.
    _parse_card: Parse a string representation of a card into its rank and suit.

"""
from __future__ import annotations

from typing import Tuple

from .enums import Rank, Suit


class Card():
    """Represents a single playing card with a rank and a suit.

    Card objects can be instantiated with a two-character string representation or a tuple of rank
    and suit (enum types defined in pyker.enums - see pyker.enums.Rank, pyker.enums.Suit

    String representation for rank and suit based on below mapping:
    Rank: 2-9: Card ranks 2-9, T - Ten, J - Jack, Q - Queen, K - King, A - Ace
    Suit: S - Spades♠︎ , H - Hearts♥︎ , C - Clubs♣︎ , D - Diamonds♦︎

    # Usage

    Create a card:
    >>> ace_spades = Card((pyker.Rank.ACE, pyker.Suit.SPADES)) # Ace of Spades
    >>> four_hearts = Card('H4') # Four of Hearts

    Display a card:
    >>> four_hearts
    <Card(rank=Rank.FOUR, suit=Suit.HEARTS) _id=1>
    >>> print(my_card)
    4♥️

    Compare cards by rank:
    >>> ten_diamonds = Card('TD') # Ten of Diamonds
    >>> nine_hearts = Card('9H') # Three of Hearts
    >>> ten_diamonds > nine_hearts
    True

    Check if cards are adjacent:
    >>> ten_diamonds @ four_hearts
    False
    >>> ten_diamonds @ nine_hearts
    True

    Check if cards are adjacent and less-that / greater-than each other:
    >>> ten_diamonds << nine_hearts
    False
    >>> ten_diamonds >> nine_hearts
    True
    """

    _id: int = 0

    def __init__(self, card_def: str | Tuple[Rank, Suit]) -> Card:
        """Initiate a Card object

        Args:
            card_def: A two-character string representation of a card, or a tuple - (Rank, Suit).
                str:    One character for rank and one for suit in any order.
                    Ex: 'AS' - Ace of Spades, 'HT' - Ten of Hearts
                tuple:  (rank, suit) - rank is a pyker.Rank enum. Suit is pyker.Suit enum.
                    Ex: Card((pyker.Rank.QUEEN, pyker.Suit.CLUBS))
        """
        match card_def:
            case str():
                parsed_card = Card._parse_card(card_def)
                self.rank: Rank = parsed_card[0]
                self.suit: Suit = parsed_card[1]
            case tuple():
                self.rank: Rank = card_def[0]
                self.suit: Suit = card_def[1]
            case _:
                raise ValueError
        Card._id += 1
        self._id: int = Card._id

    def __eq__(self: Card, other: Card) -> bool:
        """True if self is equal to other in rank"""
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self: Card, other: Card) -> bool:
        """True if self is less than other in rank"""
        if (self.rank == Rank.ACE) ^ (other.rank == Rank.ACE):
            return True
        return self.rank.number < other.rank.number

    def __gt__(self: Card, other: Card) -> bool:
        """True if self is greater than other in rank"""
        if (self.rank == Rank.ACE) ^ (other.rank == Rank.ACE):
            return True
        return self.rank.number > other.rank.number

    def __le__(self: Card, other: Card) -> bool:
        """True if self is less than or equal to other in rank"""
        return (self == other) or (self < other)

    def __ge__(self: Card, other: Card) -> bool:
        """True if self is greater than or equal to other in rank"""
        return (self == other) or (self > other)

    def __matmul__(self: Card, other: Card) -> bool:
        """Checks if self and other are adjacent in rank. Returns True if so."""
        if self == other:
            return False
        if abs(self.rank.number - other.rank.number) == 1:
            return True
        if Rank.ACE in {self.rank, other.rank}:
            if Rank.TWO in {self.rank, other.rank}:
                return True
            if Rank.KING in {self.rank, other.rank}:
                return True
        return False

    def __lshift__(self: Card, other: Card) -> bool:
        """Checks if self is adjacent and less than other in rank.
        Helpful for detecting straights"""
        if self.rank == Rank.ACE and other.rank == Rank.KING:
            return False
        if self.rank == Rank.TWO and other.rank == Rank.ACE:
            return False
        return self < other and self @ other

    def __rshift__(self: Card, other: Card) -> bool:
        """Checks if self is adjacent and greater than other in rank.
        Helpful for detecting straights"""
        if self.rank == Rank.ACE and other.rank == Rank.TWO:
            return False
        if self.rank == Rank.KING and other.rank == Rank.ACE:
            return False
        return self > other and self @ other

    def __repr__(self: Card) -> str:
        """Returns a string representation of the card instance."""
        class_name = type(self).__name__
        return f"<{class_name}(rank={self.rank}, suit={self.suit}) _id={self._id}>"

    def __str__(self: Card) -> str:
        """Returns a string representation of the card for printing."""
        return f"{self.rank.alias}{self.suit.symbol}"

    @staticmethod
    def _parse_card(card_def: str) -> Tuple[Rank, Suit]:
        """Parses a string representation of a card into its rank and suit."""
        if len(card_def.strip()) != 2:
            raise ValueError(
                'card_def must be two characters long. Ex: \'AD\'')
        enums = list(Rank) + list(Suit)
        mapping = {e.alias: e for e in enums}
        els = [mapping[e] for e in card_def]
        rank = list(filter(lambda e: isinstance(e, Rank), els))[0]
        suit = list(filter(lambda e: isinstance(e, Suit), els))[0]
        return (rank, suit)
