from nose.tools import *
from blackjack.engine import Engine
from blackjack.dealer import Dealer
from blackjack.player import Player


class TestEngine(object):
    def setup(self):
        self.game = Engine('Test Dealer', 'Test Player')

    def teardown(self):
        del self.game

    def test_engine(self):
        assert isinstance(self.game, Engine)

    def test_dealer(self):
        assert isinstance(self.game.dealer, Dealer)

    def test_player(self):
        assert isinstance(self.game.player, Player)
