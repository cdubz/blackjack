import webapp2
import json
import datetime


from blackjack.engine import *
from blackjack.models import *


class Games(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        if request.method in ('GET', 'PATCH'):
            if 'Bj-Gid' in request.headers.keys():
                # @todo Figure out how to raise a custom error for bad GID
                self.game_key = ndb.Key(urlsafe=request.headers['BJ-GID'])
                self.game = self.game_key.get()
                self.players = Player.query(ancestor=self.game_key)\
                    .order(Player.deal_order).fetch()
            else:
                raise ValueError('Game ID not provided.')

    # Create a new game
    def post(self):
        game = Game()
        add_deck(game.deck)
        game_key = game.put()

        player = Player(
            parent=game_key,
            name=self.request.get('player_name', 'Some Jerk'),
            stand=False,
            deal_order=0
        )

        dealer = Player(
            parent=game_key,
            name='Dealer 1.0',
            stand=False,
            deal_order=1
        )

        # Create initial game state
        deal(game.deck, player, False)
        deal(game.deck, dealer, False)
        deal(game.deck, player)
        deal(game.deck, dealer)
        ndb.put_multi([game, player, dealer])

        # Add the new GID to the headers and re-run __init__ to add the
        # game state objects to self.
        self.request.headers['Bj-Gid'] = game_key.urlsafe()
        self.__init__(self.request, self.response)
        self.get()

    # Provide status info for a game
    # @todo Customize the state return for the requesting player
    def get(self):
        state = {
            'GID': self.game_key.urlsafe(),
            'Started': self.game.began.isoformat(),
            'Updated': self.game.updated.isoformat(),
            'Ended': None,
            'players': {}
        }

        if self.game.ended:
            state['Ended'] = self.game.ended.isoformat()

        for player in self.players:
            state['players'][player.deal_order] = {
                'key': player.key.urlsafe(),
                'name': player.name,
                'score': player.shown_score,
                'stand': player.stand
            }

        self.send_response(state)

    # Update game state
    def patch(self):
        if self.game.ended:
            self.get()
            return

        action = self.request.headers['BJ-Action']

        to_put = []
        # @todo Add BUST logic
        for player_data in self.players:
            if not player_data.stand:
                player = player_data.key.get()

                if action == 'hit':
                    deal(self.game.deck, player)
                elif action == 'stand':
                    player.stand = True

                    # If this standing player is the last player, also end
                    # the game.
                    if player == self.players[-1]:
                        self.game.ended = datetime.datetime.today()
                else:
                    raise ValueError('Invalid action: %s' % action)

                to_put.append(player)
                break

        to_put.append(self.game)
        ndb.put_multi(to_put)

        self.get()

    # Response controller
    def send_response(self, content):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(content))


# http://stackoverflow.com/questions/16280496/
allowed_methods = webapp2.WSGIApplication.allowed_methods.union(('PATCH',))
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([('/api/v1/games', Games)], debug=True)
