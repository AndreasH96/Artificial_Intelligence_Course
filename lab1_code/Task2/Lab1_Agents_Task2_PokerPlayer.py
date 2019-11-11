__author__ = 'fyt'
import math
import random
from Lab1_Agents_Task2_Hand import Hand
# identify if there is one or more pairs in the hand

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}

class PokerPlayer:
    def __init__(self,id):
        self.Id = id
        self.cardHand = Hand(self.Id)
        
    def assignCards(self,newHand):
        self.cardHand.updateHand(newHand)
   
    def getHand(self):
        return self.cardHand

    def calculateBid(self):
        pass




