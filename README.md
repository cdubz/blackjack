# Blackjack

Blackjack on the Google App Engine with a web-based interface.

## Setup
The [Google App Engine SDK](https://cloud.google.com/appengine/downloads) is 
required to run this program.

    dev_appserver.py /path/to/blackjack

## API

The API has the following operations. All operations return a JSON response with basic, non-targeted game state information.

### POST */api/v1/games*
Begins a new game with the player identified by a *player_name* parameter if provided.

### GET */api/v1/games*
Returns basic state information about the game with ID in the header *Bj-Gid*.

### PATCH */api/v1/games*
With a *Bj-Gid* header identifying the game, the *Bj-Action* header can be either "hit" or "stand". This call will also resolve game end when every player stands (but not on bust).

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations.