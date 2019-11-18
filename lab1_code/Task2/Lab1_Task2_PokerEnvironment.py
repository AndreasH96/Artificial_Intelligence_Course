__author__ = 'fyt'
import math
import random
import json
from itertools import product
from Lab1_Agents_Task2_MemoryAgent import MemoryPokerPlayer
from Lab1_Agents_Task2_PokerPlayer_Reflex import ReflexPokerPlayer
from Lab1_Agents_Task2_PokerPlayer_Random import RandomPokerPlayer
from Lab1_Agents_Task2_PokerPlayer_Fixed import FixedPokerPlayer
from Lab1_Agents_Task2_CorrelationGenerationReflexAgent import CorrelationReflexPokerPlayer
from Lab1_Agents_Task2_PokerPlayer import PokerPlayer
from Lab1_Agents_Task2_Card import Card
from numpy import corrcoef
from numpy import array
# identify if there is one or more pairs in the hand

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}
class PokerEnvironment:
    def __init__(self, player1, player2):
        self.Player1 = player1
        self.Player2 = player2
        with open ('lab1_code\Task2\cards.json') as json_file:
            self.rankToValueJSON = json.load(json_file)['cards']
        self.Wins = {"Player1": {"Times": 0, "Amount": 0 }, "Player2": {"Times": 0, "Amount": 0 }}
        self.handValueCheckAgent = CorrelationReflexPokerPlayer()
        self.totalbids1 = []
        self.totalbids2 = []
    def generateDeck(self):
        possibleRanks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        possibleSuits = ['s', 'h', 'd', 'c']
        generatedCardDeck =[Card(rank,suit) for (rank,suit) in product(possibleRanks, possibleSuits)]
        random.shuffle(generatedCardDeck)
        return generatedCardDeck
    
    def evaluateWinner(self):
        player1Wins = {"outcome":1}
        player2Wins = {"outcome":2}
        draw = {"outcome":0}
        
        player1Hand = self.Player1.cardHand.identifyHand()
        player2Hand = self.Player2.cardHand.identifyHand()
        print("Player1 %s" % player1Hand)
        print("Player2 %s" % player2Hand)
        if player1Hand['cards'][0][2] > player2Hand['cards'][0][2]:
            return(player1Wins)
        elif player1Hand['cards'][0][2] < player2Hand['cards'][0][2]:
             return(player2Wins)
        else:
            for player1Card, player2Card in zip(player1Hand['cards'], player2Hand['cards']):
                if self.rankToValueJSON[player1Card[0]] > self.rankToValueJSON[player2Card[0]]:
                    return(player1Wins)
                elif self.rankToValueJSON[player1Card[0]] < self.rankToValueJSON[player2Card[0]]:
                    return(player2Wins)
        return(draw)

    def cardDealingPhase(self):
        cardDeck = self.generateDeck()
        self.Player1.assignCards(cardDeck[0:3])
        self.Player2.assignCards(cardDeck[3:6])

    def biddingPhase(self):
        self.Biddings = {"Player1" : [], "Player2" : [], "Total": 0}
        player1BidSum = 0
        player1ValueSum = 0 
        player2BidSum = 0
        player2ValueSum = 0
        for x in range(3):
            Player1Bid = self.Player1.calculateBid()
            Player2Bid = self.Player2.calculateBid()
            self.totalbids1.append(Player1Bid)
            self.Biddings["Player1"].append(Player1Bid)
            self.Biddings["Player2"].append(Player2Bid)
            self.Biddings["Total"] += (Player1Bid + Player2Bid)
            if("Memory" in str(type(self.Player1))):
                self.Player1.appendOpponentBid(Player2Bid)
            if("Memory" in str(type(self.Player2))):
                self.Player2.appendOpponentBid(Player1Bid)
            player1BidSum += Player1Bid 
            player1ValueSum += self.Player1.cardHand.identifyHand()["Value"]
            player2BidSum += Player2Bid
            player2ValueSum += self.Player2.cardHand.identifyHand()["Value"]

        if("Memory" in str(type(self.Player1))):
            self.Player1.appendOpponentBidsError(player2ValueSum / player2BidSum)
        if("Memory" in str(type(self.Player2))):
            self.Player2.appendOpponentBidsError(player1ValueSum / player1BidSum)
        
    def showDownPhase(self):
        result = self.evaluateWinner()['outcome']
        if result == 1:
            print("Player1 wins %s$" % (self.Biddings["Total"]))
            self.Wins["Player1"]["Amount"] += self.Biddings["Total"]
            self.Wins["Player1"]["Times"]  += 1
        elif result == 2:
            print("Player2 wins %s$" % (self.Biddings["Total"]))
            self.Wins["Player2"]["Amount"] += self.Biddings["Total"]
            self.Wins["Player2"]["Times"]  += 1
        else:
            print("It's a draw" )
        



    def generateCorrelationComparisonPlays(self):
            randomPlayer = RandomPokerPlayer()
            fixedPlayer = FixedPokerPlayer()
            reflexPlayer = ReflexPokerPlayer()
            players = [randomPlayer,fixedPlayer,reflexPlayer]
            datastore = {"RandomPokerPlayer": [], "FixedPokerPlayer":[], "ReflexPokerPlayer":[]}
            for x in range(1000):
                deck = self.generateDeck()
                for playerIndex in range(3):
                    players[playerIndex].assignCards(deck[0:3])
                #playerBiddings = []
                
                for player in players:
                    bettingSum = 0
                    handValueSum = 0
                    for x in range(3):
                        #playerBiddings.append(player.calculateBid())
                        bettingSum +=  player.calculateBid()
                        handValueSum += player.cardHand.identifyHand()["Value"]
                    if("Reflex" in str(type(player))):
                        datastore["ReflexPokerPlayer"].append(handValueSum/bettingSum)
                        #datastore["ReflexPokerPlayer"].append(bettingSum /3)
                    elif("Fixed" in str(type(player))):
                        datastore["FixedPokerPlayer"].append(handValueSum/bettingSum)
                        #datastore["FixedPokerPlayer"].append(bettingSum /3)
                        #self.totalbids2.append()
                    elif("Random" in str(type(player))):
                        datastore["RandomPokerPlayer"].append(handValueSum/bettingSum)   
                        #datastore["RandomPokerPlayer"].append(bettingSum /3)
                    #playerBiddings=[]
            with open("lab1_code\Task2\correlationComparison.json", 'w') as jsonFile:
                json.dump(datastore,jsonFile)

    def start(self):

        for x in range(1000):
            self.cardDealingPhase()
            self.biddingPhase()
            self.showDownPhase()
            print(self.Biddings)
        print (self.Wins)


        





