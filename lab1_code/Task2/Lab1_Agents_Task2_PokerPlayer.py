__author__ = 'fyt'
import math
import random
from Lab1_Agents_Task2_Hand import Hand
import json

class PokerPlayer:
    def __init__(self):
        self.cardHand = Hand()
        with open ('lab1_code\Task2\cards.json') as json_file:
            self.rankToValueJSON = json.load(json_file)['cards']
    def assignCards(self,newHand):
        self.cardHand.updateHand(newHand)
   
    def getHand(self):
        return self.cardHand

    def calculateBid(self):
        print("No player type specified")
