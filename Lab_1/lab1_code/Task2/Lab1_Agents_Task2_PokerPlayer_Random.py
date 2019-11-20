__author__ = 'fyt'
import math
import random
from Lab1_Agents_Task2_PokerPlayer import PokerPlayer

class RandomPokerPlayer(PokerPlayer):
    
    def __init__(self):
        super().__init__()
        self.type = "Random"
    def calculateBid(self):
        amount = random.randint(0,50)
        return amount

