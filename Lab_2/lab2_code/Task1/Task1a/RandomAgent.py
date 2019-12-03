import numpy as np
import math
import heapq
from Node import Node
from SearchAgent import SearchAgent
class RandomAgent(SearchAgent):
    def __init__(self, searchMap = None, startPosition = None, goalPosition= None):
        super().__init__(searchMap, startPosition, goalPosition)
        self.description = "Random Search Algorithm"
        self.returnToPreviousAllowed = False
    def addNode(self,node):
        self.nodeList.append(node)
        self.nodeList.sort(key= lambda node: node.cost)
    def getNextNode(self):
        returnNode = self.nodeList[0]
        self.nodeList.remove(returnNode)
        return returnNode
    def getType(self):
        return type(self).__name__
    def calculateCost(self,nodeCoordinates):
        return np.random.randint(1,5)
    
    
                    
    