__author__ = 'fyt'
import math
import random
from Lab1_Agents_Task2_PokerPlayer import PokerPlayer
class ReflexPokerPlayer(PokerPlayer):
    
    def calculateBid(self):
        handAnalysis = self.cardHand.identifyHand()
        amount = (handAnalysis["cards"][0][2] - 1)*19 + self.rankToValueJSON[handAnalysis["cards"][0][0]]-2
        return amount

