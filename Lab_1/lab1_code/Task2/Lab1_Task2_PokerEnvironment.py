__author__ = 'fyt'
import math
import random
import json
from itertools import product
from Lab1_Agents_Task2_MemoryAgent import MemoryPokerPlayer
from Lab1_Agents_Task2_PokerPlayer_Reflex import ReflexPokerPlayer
from Lab1_Agents_Task2_PokerPlayer_Random import RandomPokerPlayer
from Lab1_Agents_Task2_PokerPlayer_Fixed import FixedPokerPlayer
from Lab1_Agents_Task2_PokerPlayer import PokerPlayer
from Lab1_Agents_Task2_Card import Card
from numpy import corrcoef
from numpy import array
from matplotlib import pyplot as plt 
import numpy as np  
   

# identify if there is one or more pairs in the hand

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}
class PokerEnvironment:
    def __init__(self, player1, player2):
        self.Player1 = player1
        self.Player2 = player2
        with open ('lab1_code\Task2\cards.json') as json_file:
            self.rankToValueJSON = json.load(json_file)['cards']
        self.Wins = {"Player1": {"Times": 0, "Amount": 0 , "PlayerType": self.Player1.type}, "Player2": {"Times": 0, "Amount": 0 , "PlayerType": self.Player2.type }}
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
        
    def clearHistogramJSON(self):
        with open ('lab1_code/Task2/fixedAndRandomComparison.json' , 'w') as data_file:
            emptyjsonDacta = {"Player1":[],"Player2":[]}
            json.dump(emptyjsonDacta,data_file)

    def start(self):

        self.clearHistogramJSON()

        for x in range(200):
            self.Wins = {"Player1": {"Times": 0, "Amount": 0 , "PlayerType": self.Player1.type}, "Player2": {"Times": 0, "Amount": 0 , "PlayerType": self.Player2.type }}
            for y in range(50):
                self.cardDealingPhase()
                self.biddingPhase()
                self.showDownPhase()
            with open ('lab1_code/Task2/fixedAndRandomComparison.json' ) as data_file:
                jsonData = json.load(data_file)
                
            with open ('lab1_code/Task2/fixedAndRandomComparison.json' , 'w') as data_file:

                for playerResult in self.Wins.items():
                    print("%s of Type: %s Won: %s times and walked away with: %s$ evaluating to a money/win ratio of %s \n" % 
                    (playerResult[0], playerResult[1]["PlayerType"], playerResult[1]["Times"], playerResult[1]["Amount"], round(playerResult[1]["Amount"]/playerResult[1]["Times"],2) ))
                    jsonData[playerResult[0]].append(round(playerResult[1]["Amount"]/playerResult[1]["Times"],2))
                json.dump(jsonData,data_file)
        
        with open ('lab1_code/Task2/fixedAndRandomComparison.json' ) as data_file:
                jsonData = json.load(data_file)
        
                player1HistogramData = jsonData["Player1"]
                player1HistogramDataRange = np.arange(round(np.min(player1HistogramData) - 5 ,2),round(np.max(player1HistogramData) + 5, 2 ),1)

                player2HistogramData = jsonData["Player2"]
                player2HistogramDataRange = np.arange(round(np.min(player2HistogramData) - 5 ,2),round(np.max(player2HistogramData) + 5, 2 ),1)
                
                
                plt.hist(player1HistogramData, bins = player1HistogramDataRange , lw=3, fc=(0, 0, 1, 0.5)) 
                plt.hist(player2HistogramData, bins = player2HistogramDataRange, lw=3, fc=(1, 0, 0, 0.5)) 
                plt.title("Blue: Fixed, Orange: Random") 
                plt.xlabel("Money per win")
                plt.ylabel("Amount of times")
                #plt.savefig('fixedRandomComparison.png')
                plt.show()