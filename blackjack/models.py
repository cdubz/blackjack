from google.appengine.ext import ndb


class Card(ndb.Model):
    name = ndb.StringProperty()
    shown = ndb.BooleanProperty()
    value = ndb.IntegerProperty()
    suit = ndb.StringProperty()


class Player(ndb.Model):
    deal_order = ndb.IntegerProperty()
    name = ndb.StringProperty()
    hand = ndb.StructuredProperty(Card, repeated=True)
    stand = ndb.BooleanProperty()
    shown_score = ndb.IntegerProperty()
    total_score = ndb.IntegerProperty()


class Game(ndb.Model):
    deck = ndb.StructuredProperty(Card, repeated=True)
    began = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
