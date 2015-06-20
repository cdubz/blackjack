from sys import exit
from time import sleep

from dealer import Dealer
from player import Player
from blackjack.deck import Deck


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

    # noinspection PyMethodMayBeStatic
    def update_scores(self, player):
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

    def play(self):
        self.deck.shuffle()
        self.deal_from_top(self.player, False)
        self.deal_from_top(self.dealer, False)
        self.deal_from_top(self.player)
        self.deal_from_top(self.dealer)

        while not self.player.stand:
            self.print_status()
            action = raw_input('hit or stand? > ')

            if action == 'hit':
                self.deal_from_top(self.player)

                # If the player exceeds 21 in shown_score, there is no reason
                # to continue the game, so this is checked after each hit.
                if self.player.shown_score > 21:
                    self.end_game()

            elif action == 'stand':
                self.player.stand = True

        while not self.dealer.stand:
            self.print_status()

            # Add a small delay so that all the status prints do not overwhelm
            # the player.
            sleep(2)

            # This simple logic does not take in to account any probability.
            # The total_score of 19 is just a basic safety and the dealer
            # will take (potentially stupid) risks to beat the player.
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
        print "%s's score: %i" % (self.dealer.name, self.dealer.total_score)
        print "%s's score: %i" % (self.player.name, self.player.total_score)

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

            # Re-run init to clear scores and create a new Deck.
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
