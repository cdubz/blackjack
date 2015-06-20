from engine import Engine

print 'What is your name?'
player_name = raw_input('> ') or 'Rude Player'

print "Hello %s! What is your dealer's name?" % player_name
dealer_name = raw_input('> ') or 'Mr. Dealer'

game = Engine(dealer_name, player_name)
game.play()
