import webapp2
import json


from blackjack.engine import *
from blackjack.models import *


class Games(webapp2.RequestHandler):

    # Create a new game
    def post(self):
        game = Game()
        add_deck(game.deck)
        game_key = game.put()

        player = Player(
            parent=game_key,
            name=self.request.get('player_name', 'Anonymoose'),
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

        # Return GID only
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({'GID': game_key.urlsafe()}))

    # Provide status info for a game
    def get(self):
        gid = self.request.headers['BJ-GID']
        game_key = ndb.Key(urlsafe=gid)
        game = game_key.get()
        players = Player.query(ancestor=game_key).order(Player.deal_order).fetch()

        state = {
            'GID': gid,
            'Started': game.began.isoformat(),
            'Updated': game.updated.isoformat(),
            'players': {}
        }
        for player in players:
            state['players'][player.deal_order] = {
                'key': player.key.urlsafe(),
                'name': player.name,
                'score': player.shown_score,
                'stand': player.stand
            }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(state))

    # Update game state
    def patch(self):
        gid = self.request.headers['BJ-GID']
        action = self.request.headers['BJ-Action']
        game_key = ndb.Key(urlsafe=gid)
        game = game_key.get()
        players = Player.query(ancestor=game_key).order(Player.deal_order).fetch()

        to_put = []
        for player_data in players:
            if not player_data.stand:
                player = player_data.key.get()

                if action == 'hit':
                    deal(game.deck, player)
                elif action == 'stand':
                    player.stand = True
                else:
                    raise ValueError('Invalid action: %s' % action)

                to_put.append(player)
                break

        if to_put:
            to_put.append(game)
            ndb.put_multi(to_put)
        else:
            raise StandardError('All players stand. Game is ended.')

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'GID': game_key.urlsafe(),
            'action': action
        }))


# http://stackoverflow.com/questions/16280496/
allowed_methods = webapp2.WSGIApplication.allowed_methods.union(('PATCH',))
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([('/api/v1/games', Games)], debug=True)
