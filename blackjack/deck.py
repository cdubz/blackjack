from random import shuffle


class Deck(object):

    def __init__(self):
        self.cards = []

        # The range() below is mapped to strings to keep the list element
        # types consistent. Card() will map them to ints.
        for name in map(str, range(2, 11)) + ['J', 'Q', 'K', 'A']:
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

        # The name will set value for all but A (11), J, Q, and K (10 each).
        if name == 'A':
            self.value = 11
        elif name == 'J' or name == 'Q' or name == 'K':
            self.value = 10
        else:
            self.value = int(name)

        # Creates unicode strings for suit characters for nicer output.
        if suit == 'spades':
            self.suit = u'\u2660'
        elif suit == 'hearts':
            self.suit = u'\u2665'
        elif suit == 'diamonds':
            self.suit = u'\u2666'
        elif suit == 'clubs':
            self.suit = u'\u2663'
