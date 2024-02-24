"""Pyker: A Python package for cards/CardSet management and poker hand scoring.

Pyker provides classes and functions for managing cards, evaluating poker hands, and
performing various operations related to card games.

Classes:
    - Card: Represents a playing card with a rank and a suit.
    - CardSet: Represents a collection of cards.

Enums:
    - Suit: Enumerates the four suits in a standard Deck of cards (Spades, Hearts, Clubs, Diamonds).
    - Rank: Enumerates the ranks of cards in a standard Deck (Ace through King).
    - HandType: Enumerates the possible types of poker hands.

Usage:
    To use Pyker, simply import the desired classes and functions from the pyker module:

    >>> from pyker.CardSet import CardSet
    >>> from pyker.card import Card
    >>> from pyker.enums import Suit, Rank, HandType

    # Example usage:
    >>> deck = CardSet()
    >>> deck.shuffle()
    >>> hand = deck.deal(5)


    # Hold'em example
    >>> deck = CardSet()
    >>> deck.suffle()
    >>> player_1 = deck.deal(2)
    >>> player_2 = deck.deal(2)
    >>> table_cards = deck.deal(5)
    >>> p1_best_hand = (player_1 + table_cards).best_hand
    >>> p2_best_hand = (player_2 + table_cards).best_hand
    >>> if (p1_best_hand > p2_best_hand):
    >>>     result = "Player 1 wins"
    >>> elif (p1_best_hand == p2_best_hand):
    >>>     result = "Tie"
    >>> else:
    >>>     result = "Player 2 wins"


For more detailed documentation and examples, please refer to the individual modules and classes
within the package.
"""

from .enums import Suit, Rank, HandType
from .card import Card
from .card_set import CardSet
from .scored_hand import ScoredHand
