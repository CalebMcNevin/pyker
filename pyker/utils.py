from .enums import Rank


def sort_cards_by_rank(cards, aces_high=True):
    return sorted(cards,
                  reverse=True,
                  key=lambda card: card.rank.number
                  if not aces_high else (card.rank.number
                                         if card.rank != Rank.ACE else 14))
