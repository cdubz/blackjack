from random import shuffle

class Deck(object):

    def __init__(self):
        self.cards = []
        for name in range(2,11) + ['J', 'Q', 'K', 'A']:
            self.cards.append(Card('spades', name))
            self.cards.append(Card('hearts', name))
            self.cards.append(Card('diamonds', name))
            self.cards.append(Card('clubs', name))

    def shuffle(self):
        shuffle(self.cards)

    def deal_from_top(self):
        return self.cards.pop()


class Card(object):

    def __init__(self, suit, name):
        self.name = name
        self.shown = False

        # The name will set value for all but A, K, Q, and J
        if name == 'A':  # Need a way to do this differently, a function?
            self.value = 11
        elif name == 'J' or name == 'Q' or name == 'K':
            self.value = 10
        else:
            self.value = name

        if suit == 'spades':
            self.suit = u'\u2660'
        elif suit == 'hearts':
            self.suit = u'\u2665'
        elif suit == 'diamonds':
            self.suit = u'\u2666'
        elif suit == 'clubs':
            self.suit = u'\u2663'
