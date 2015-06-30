from random import shuffle
from blackjack.models import *


def add_deck(deck):
    for name in map(str, range(2, 11)) + ['J', 'Q', 'K', 'A']:
        if name == 'A':
            value = 11
        elif name == 'J' or name == 'Q' or name == 'K':
            value = 10
        else:
            value = int(name)

        for suit in ['S', 'H', 'D', 'C']:
            deck.append(Card(
                suit=suit,
                name=name,
                value=value,
                shown=False
            ))

    shuffle(deck)

def deal(deck, player, shown=True):
    card = deck.pop()
    card.shown = shown
    player.hand.append(card)

    update_scores(player)

def update_scores(player):
    player.shown_score = 0
    player.total_score = 0
    high_ace_indexes = []

    for idx, card in enumerate(player.hand):

        # Track the aces with a value of 11 so they can be evaluated for
        # a potential decrease to 1 in the next block.
        if card.name == 'A' and card.value == 11:
            high_ace_indexes.append(idx)

        if card.shown:
            player.shown_score += card.value

        player.total_score += card.value

    # Because aces can be 11 or 1, we must evaluate and optimize their value
    # if the player has exceeded 21.
    for idx in high_ace_indexes:
        if player.total_score > 21:
            player.hand[idx].value = 1
            player.total_score -= 10

            if player.hand[idx].shown:
                player.shown_score -= 10
