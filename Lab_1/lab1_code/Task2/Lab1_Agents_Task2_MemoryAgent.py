__author__ = 'fyt'
import math
from numpy import corrcoef
from numpy import array
import random
import operator
import matplotlib.pyplot as plt
import json
from Lab1_Agents_Task2_PokerPlayer import PokerPlayer

class MemoryPokerPlayer(PokerPlayer):
    def __init__(self):
        super().__init__()
        self.truePreviousOpponentPlays = []
        self.estimatedPreviousOpponentPlays= []
        self.handValuesComparedToBidsOfPreviosOpponent = []
        self.biddingFactor = 1
        self.type="Memory"

    def assignCards(self,newHand):
        self.biddingFactor = 1
        self.cardHand.updateHand(newHand)
   
    def calculateBid(self):
        handAnalysis = self.cardHand.identifyHand()
        amount = (handAnalysis["cards"][0][2] - 1)*19 + self.rankToValueJSON[handAnalysis["cards"][0][0]]-2
        return round(amount * self.biddingFactor,0)

    def appendOpponentBid(self,opponentBid):
        ownBid = self.calculateBid()
        if opponentBid > ownBid:
            self.biddingFactor *= ownBid/(opponentBid*2)
        else :
            self.biddingFactor = 1


    def estimateOpponentHand(self,opponentBid):
        estimatedPairing = int(opponentBid / 19)
        esimatedHighestCard = (opponentBid% 19) + 2
        print("Estimated paring : %s Estimated card : %s" % ( estimatedPairing, esimatedHighestCard))
        return ((estimatedPairing,esimatedHighestCard))
   