# Blackjack (gae-web development branch)

Blackjack on the Google App Engine with a web-based interface.

There is currently no real end game condition. If all players stand, PATCH 
calls to the API will raise an error. Otherwise, things will probably break 
for now.

## Setup
The [Google App Engine SDK](https://cloud.google.com/appengine/downloads) is 
required to run this program.

    dev_appserver.py /path/to/blackjack

## API

The basic API has the following operations:

### POST */api/v1/games*
With a "player_name" parameter, begins a new game and returns a Game ID in a 
JSON array in the body.

### GET */api/v1/games*
With a BJ-GID header containing a Game ID, returns some basic state information 
about the game in a JSON array in the body.

### PATCH */api/v1/games*
With a BJ-GID header containing a Game ID and a BJ-Action header containing 
either "hit" or "stand", updates the game state based the current game state. 
On success, returns a JSON array containing the BJ-GID and BJ-Action headers.

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations.