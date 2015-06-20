from dealer import Dealer
from player import Player
from deck import Deck
from sys import exit
from time import sleep

class Engine(object):

    def __init__(self, dealer_name, player_name):
        self.dealer = Dealer(dealer_name)
        self.player = Player(player_name)
        self.deck = Deck()

    def deal_from_top(self, deal_to, show=True):
        deal_to.hand.append(self.deck.deal_from_top())

        if show:
            deal_to.hand[-1].shown = True

        self.update_scores(deal_to)

    def update_scores(self, player):
        player.shown_score = 0
        player.total_score = 0
        high_ace_indexes = []

        for idx, card in enumerate(player.hand):
            if card.name == 'A' and card.value == 11:
                high_ace_indexes.append(idx)

            if card.shown:
                player.shown_score += card.value

            player.total_score += card.value

        # If the score exceeds 21, check for 11 aces and adjust
        for idx in high_ace_indexes:
            if player.total_score > 21:
                player.hand[idx].value = 1
                player.total_score -= 10

                # Check if the ace is part of the shown score and update
                # there too if necessary.
                if player.hand[idx].shown:
                    player.shown_score -= 10

    def play(self):
        # Deal first cards
        self.deck.shuffle()
        self.deal_from_top(self.player, False)
        self.deal_from_top(self.dealer, False)
        self.deal_from_top(self.player)
        self.deal_from_top(self.dealer)

        # Deal to player
        while not self.player.stand:
            self.print_status()
            action = raw_input('hit or stand? > ')

            if action == 'hit':
                self.deal_from_top(self.player)

                # Check for bust
                if self.player.shown_score > 21:
                    self.end_game()

            elif action == 'stand':
                self.player.stand = True

        # Deal to dealer
        while not self.dealer.stand:
            self.print_status()
            sleep(2)

            if self.dealer.shown_score > 21:
                self.end_game()
            elif self.dealer.total_score > 19:
                self.dealer.stand = True
            elif self.dealer.total_score <= self.player.shown_score:
                self.deal_from_top(self.dealer)
            else:
                self.deal_from_top(self.dealer)

        self.end_game()

    def end_game(self):
        print 'Game over.'
        print "%s's score: %i" %(self.dealer.name, self.dealer.total_score)
        print "%s's score: %i" %(self.player.name, self.player.total_score)

        if self.player.total_score >= 21:
            print 'YOU BUSTED!'
        elif (self.player.total_score > self.dealer.total_score
              or self.dealer.total_score > 21):
            print 'YOU WON!!!'
        else:
            print 'You lose. Better luck next time.'

        print 'Would you like to play again?'
        response = raw_input('yes or no? > ')

        if response == 'yes':
            self.__init__(self.dealer.name, self.player.name)
            self.play()
        else:
            exit(0)

    def print_status(self):
        print 'Dealer Name:', self.dealer.name
        print 'Dealer Score (shown):', self.dealer.shown_score
        print 'Dealer Hand:'
        for card in self.dealer.hand:
            if card.shown:
                print card.name, card.suit
            else:
                print '[ ]'

        print 'Player Name:', self.player.name
        print 'Dealer Score (shown):', self.player.shown_score
        print 'Player Score (total):', self.player.total_score

        print 'Player Hand:'
        for card in self.player.hand:
            print card.name, card.suit
