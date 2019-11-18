__author__ = 'fyt'
import math
from numpy import corrcoef
from numpy import array
import random
import operator
import matplotlib.pyplot as plt
import json
from Lab1_Agents_Task2_PokerPlayer import PokerPlayer
from Lab1_Agents_Task2_CorrelationGenerationReflexAgent import CorrelationReflexPokerPlayer
class MemoryPokerPlayer(PokerPlayer):

    def __init__(self):
        super().__init__()
        self.truePreviousOpponentPlays = []
        self.estimatedPreviousOpponentPlays= []
        self.handValueCheckAgent = CorrelationReflexPokerPlayer()
        self.handValuesComparedToBidsOfPreviosOpponent = []
        try:
            with open ('lab1_code\Task2\correlationComparison.json') as json_file:
                self.corralationComparison = json.load(json_file)
        except:
            with open ('lab1_code\Task2\correlationComparison.json') as json_file:
                self.corralationComparison = json.load(json_file)

    def calculateBid(self):
        handAnalysis = self.cardHand.identifyHand()
        amount = (handAnalysis["cards"][0][2] - 1)*19 + self.rankToValueJSON[handAnalysis["cards"][0][0]]-2
        return amount
    def appendOpponentBidsError(self, bidError):
        self.handValuesComparedToBidsOfPreviosOpponent.append(bidError)
        print(bidError)
    def appendOpponentBid(self,opponentBid):

        self.estimatedPreviousOpponentPlays.append({"Bid": opponentBid, "Hand":"unknown"})
        estimatedOpponentHand = self.estimateOpponentHand(opponentBid)

    def estimateOpponentHand(self,opponentBid):
        estimatedPairing = int(opponentBid / 19)
        esimatedHighestCard = (opponentBid% 19) + 2
        print("Estimated paring : %s Estimated card : %s" % ( estimatedPairing, esimatedHighestCard))
        return ((estimatedPairing,esimatedHighestCard))
    def appendOpponentBidsAndHand(self,opponentBids,opponentHand):
        self.truePreviousOpponentPlays.append({"Bids": opponentBids, "Hand":opponentHand})
        
        self.handValuesComparedToBidsOfPreviosOpponent.append(opponentHand["Value"]/opponentBids)
        #self.handValuesComparedToBidsOfPreviosOpponent.append(self.handValueCheckAgent.calculateBid(opponentHand) -opponentBids)
    def evaluateOpponent(self):
        #print("ERROR OF CURRENT %s" %(array(self.errorOfPreviosOpponentHands)))
        #print ("ERROR OF JSON %s" %(array(self.corralationComparison["FixedPokerPlayer"])))
        correlations = {
            "Random": corrcoef(array(self.corralationComparison["RandomPokerPlayer"]),array(self.handValuesComparedToBidsOfPreviosOpponent)),
            "Fixed": corrcoef(array(self.corralationComparison["FixedPokerPlayer"]),array(self.handValuesComparedToBidsOfPreviosOpponent)),
            "Reflex":  corrcoef(array(self.corralationComparison["ReflexPokerPlayer"]),array(self.handValuesComparedToBidsOfPreviosOpponent))
            }
        """ correlations["Random"] = (correlations["Random"])[0,1]
        correlations["Fixed"] = (correlations["Fixed"])[0,1]
        correlations["Reflex"] = (correlations["Reflex"])[0,1]
        """
        print ("Corralation: Random: %s  "%  (correlations["Random"]))
        print ("Corralation: Fixed: %s  "%  (correlations["Fixed"]))
        print ("Corralation: Reflex: %s  "%  (correlations["Reflex"]))
        

        """max_value=max(correlations.values())
        max_keys = [k for k, v in correlations.items() if v == max_value]
        print(max_keys ,max_value )"""
        
    
