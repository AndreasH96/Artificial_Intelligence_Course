__author__ = 'fyt'
import math
import random
from Lab1_Agents_Task2_PokerPlayer import PokerPlayer

class FixedPokerPlayer(PokerPlayer):
    def __init__(self):
        super().__init__()
        self.biddingStepValue = 1
    def calculateBid(self):
        amount = 10 * self.biddingStepValue
        self.biddingStepValue +=1
        if self.biddingStepValue == 4:
            self.biddingStepValue = 1
        return amount
