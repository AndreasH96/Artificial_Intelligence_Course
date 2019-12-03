import numpy as np
import math
import heapq
from Node import Node
from SearchAgent import SearchAgent
class BreadthFirstAgent(SearchAgent):
    def __init__(self, searchMap = None, startPosition = None, goalPosition= None):
        super().__init__(searchMap, startPosition, goalPosition)
        self.description = "Breadth First Algorithm"
        self.returnToPreviousAllowed = False
    def getType(self):
        return type(self).__name__
    def addNode(self,node):
        self.nodeList.append(node)
    def getNextNode(self):
        returnNode = self.nodeList[0]
        self.nodeList.remove(returnNode)
        return returnNode
    def calculateCost(self,nodeCoordinates):
        return 1


    
