__author__ = 'fyt'
import math
import random
from itertools import product
from Lab1_Agents_Task2_PokerPlayer_Random import RandomPokerPlayer
from Lab1_Agents_Task2_PokerPlayer import PokerPlayer
from Lab1_Agents_Task2_Card import Card
# identify if there is one or more pairs in the hand

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}
class PokerEnvironment:

    def __init__(self, player1, player2):
        self.Player1 = player1
        self.Player2 = player2
        self.Biddings = {"Player1" : [], "Player2" : []}
    def generateDeck(self):
        possibleRanks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        possibleSuits = ['s', 'h', 'd', 'c']
        generatedCardDeck =[Card(rank,suit) for (rank,suit) in product(possibleRanks, possibleSuits)]
        #random.shuffle(generatedCardDeck)
        """for card in generatedCardDeck:
            print ("rank: %s suit: %s" % (card.rank, card.suit))"""
        return generatedCardDeck
    

    def evaluateWinner(self):
        self.Player1.cardHand.analyseHand()
        self.Player2.cardHand.analyseHand()

    def cardDealingPhase(self):
        cardDeck = self.generateDeck()

        #self.Player1.assignCards(cardDeck[0:3])
        self.Player1.assignCards(cardDeck[0:3])
        self.Player2.assignCards(cardDeck[3:6])

    def biddingPhase(self):
        for x in range(3):
            Player1Bid = self.Player1.calculateBid()
            Player2Bid = self.Player2.calculateBid()
            self.Biddings["Player1"].append(Player1Bid)
            self.Biddings["Player2"].append(Player2Bid)

    def showDownPhase(self):
        self.evaluateWinner()

    def start(self):
        self.cardDealingPhase()
        self.biddingPhase()
        self.showDownPhase()
player1 = RandomPokerPlayer(1)
player2 = RandomPokerPlayer(2)
environment = PokerEnvironment(player1,player2)
environment.start()



