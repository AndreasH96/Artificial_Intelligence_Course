__author__ = 'fyt'
import math
import random
from Lab1_Agents_Task2_PokerPlayer import PokerPlayer
class MemoryPokerPlayer(PokerPlayer):

    def __init__(self):
        super().__init__()
        self.truePreviousOpponentPlays = []
        self.estimatedPreviousOpponentPlays= []

    def calculateBid(self):
        handAnalysis = self.cardHand.identifyHand()
        amount = (handAnalysis["cards"][0][2] - 1)*19 + self.rankToValueJSON[handAnalysis["cards"][0][0]]-2
        return amount

    def appendOpponentBid(self,opponentBid):
        self.estimatedPreviousOpponentPlays.append({"Bid": opponentBid, "Hand":"unknown"})
        estimatedOpponentHand = self.estimateOpponentHand(opponentBid)
    def estimateOpponentHand(self,opponentBid):
        estimatedPairing = round(opponentBid / 19,0)
        esimatedHighestCard = opponentBid % 19
        print("Estimated paring : %s Estimated card : %s" % ( estimatedPairing, esimatedHighestCard))
        return ((estimatedPairing,esimatedHighestCard))
    def appendOpponentBidAndHand(self,opponentBid,opponentHand):
        self.truePreviousOpponentPlays.append({"Bid": opponentBid, "Hand":opponentHand})
    def evaluateOpponent(self):
        pass
