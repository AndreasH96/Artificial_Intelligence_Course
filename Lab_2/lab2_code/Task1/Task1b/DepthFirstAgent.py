import numpy as np
import math
import heapq
from Node import Node
from SearchAgent import SearchAgent
class DepthFirstAgent(SearchAgent):
    def __init__(self, searchMap, startPosition, goalPosition):
        super().__init__(searchMap, startPosition, goalPosition)
        self.description = "Depth First Search Algorithm"
        self.returnToPreviousAllowed = False
    def addNode(self,node):
        self.nodeList.append(node)
    def getNextNode(self):
        returnNode = self.nodeList[len(self.nodeList) -1]
        self.nodeList.remove(returnNode)
        return returnNode
    def calculateCost(self,nodeCoordinates):
        return 1
        
    
    


