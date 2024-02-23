f"""Pyker: A Python package for cards/deck management and poker hand scoring.

Pyker provides classes and functions for managing decks of cards, evaluating poker hands, and performing various operations related to card games.

Classes:
    - Card: Represents a playing card with a rank and a suit.
    - Deck: Represents a collection of cards.

Enums:
    - Suit: Enumerates the four suits in a standard deck of cards (Spades, Hearts, Clubs, Diamonds).
    - Rank: Enumerates the ranks of cards in a standard deck (Ace through King).
    - HandType: Enumerates the possible types of poker hands.

Usage:
    To use Pyker, simply import the desired classes and functions from the pyker module:

    >>> from pyker.deck import Deck
    >>> from pyker.card import Card
    >>> from pyker.enums import Suit, Rank, HandType

    # Example usage:
    >>> deck = Deck()
    >>> deck.shuffle()
    >>> hand = deck.deal(5)


    # Hold'em example
    >>> deck = Deck()
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


For more detailed documentation and examples, please refer to the individual modules and classes within the package.
"""

from itertools import product, groupby, combinations
from random import shuffle, seed
from functools import total_ordering
from collections import Counter
from typing import Tuple

from .enums import Suit, Rank, HandType
from .card import Card
from .deck import Deck
from .scored_hand import ScoredHand
