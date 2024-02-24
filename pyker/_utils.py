"""Utility functions for the Pyker package.

This module provides various utility functions used throughout the Pyker package for common tasks
related to playing cards and poker hands.

Functions:
    sort_cards_by_rank: Sort a list of cards by their ranks. Consider Aces as high unless otherwise
        specified.
"""

from .enums import Rank
from .card import Card


def sort_cards_by_rank(cards: list[Card], aces_high: bool = True) -> None:
    """Sort a list of cards by their ranks. Consider Aces as high unless aces_high = False.

    Args:
        cards (list[Card]): A list of Card objects to be sorted.
        aces_high (bool, optional): Whether Aces should be considered as high. Defaults to True.

    Returns:
        None: This function modifies the input list in place and does not return a value.
    """
    return sorted(cards,
                  reverse=True,
                  key=lambda card: card.rank.number
                  if not aces_high else (card.rank.number
                                         if card.rank != Rank.ACE else 14))
