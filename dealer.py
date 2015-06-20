class Dealer(object):

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.stand = False
        self.shown_score = 0
        self.total_score = 0