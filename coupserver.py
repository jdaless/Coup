from enum import Enum
import random
from flask import Flask, request, jsonify

class Card(Enum):
    AMBASSADOR = 1
    ASSASSIN = 2
    CAPTAIN = 3
    CONTESSA = 4
    DUKE = 5

class ServerStatus(Enum):
    WAIT_FOR_PLAYERS = 0
    WAIT_FOR_MOVE = 1
    WAIT_FOR_RESPONSES = 2
    WAIT_FOR_SELECTION = 3

class Player:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.influence = []
    
    def selectCard(self):
        # select one of the player's influence
        return

class Game:
    def __init__(self, players):
        self.shownCards = []
        self.deck = [Card.AMBASSADOR,Card.ASSASSIN,Card.CAPTAIN,Card.CONTESSA,Card.DUKE] * 3
        random.shuffle(self.deck)
        self.players = random.shuffle(players)
        for p in players:
            p.coin = 2
            p.draw(self.deck, 2)
    
    def draw(self, actor, cards):
        for i in range(0, cards):
            actor.influence = actor.influence + cards.pop()

    def loseInfluence(self, actor, card = None):
        if(card):
            actor.influence.remove(card)
            self.shownCards.append(card)
        elif len(actor.influence) == 1:
            self.shownCards.append(actor.influence.pop())
        else:
            selectedCard = actor.selectCard()
            actor.influence.remove(selectedCard)
            self.shownCards.append(selectedCard)
            return

    def dropCards(self, actor, cards):
        selectedCard = actor.selectCard()
        actor.influence.remove(selectedCard)
        self.deck.append(selectedCard)

    def call(self, actor, target, card):
        if card in target.influence:
            self.loseInfluence(target)
        else:
            self.loseInfluence(target, card)
            self.draw(target, 1)
            self.loseInfluence(actor)

    def income(self, actor):
        actor.coin = actor.coin + 1

    def foreignAid(self, actor):
        actor.coin = actor.coin + 2

    def coup(self, actor, target):
        actor.coin = actor.coin - 7
        target.loseInfluence(1)

    def tax(self, actor):
        actor.coin = actor.coin + 3

    def assassinate(self, actor, target):
        actor.coin = actor.coin - 3
        self.loseInfluence(actor)

    def exchange(self, actor):
        actor.draw(self.deck, 2)
        self.dropCards(actor, 2)

    def steal(self, actor, target):
        if target.coin > 1:
            target.coin = target.coin - 2
            actor.coin = actor.coin + 2
        elif target.coin == 1:
            target.coin = target.coin -1
            actor.coin = actor.coin + 1

class Server:
    def __init__(self):
        app = Flask(__name__)
        self.players = []
        self.status = ServerStatus.WAIT_FOR_PLAYERS

        @app.route('/new-player')
        def newPlayer():
            self.players.append(Player(request.remote_addr, request.args.get('name','')))
            return 'success'
        
        app.run()

s = Server()