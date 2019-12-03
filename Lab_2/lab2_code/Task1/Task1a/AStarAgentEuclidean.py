import numpy as np
import math
import heapq
from Node import Node
from SearchAgent import SearchAgent
class AStarAgentEuclidean(SearchAgent):

    def __init__(self, searchMap = None, startPosition = None, goalPosition= None):
        super().__init__(searchMap, startPosition, goalPosition)
        self.description = "A* Euclidean"
        self.returnToPreviousAllowed = True
        
    def addNode(self,node):
        self.nodeList.append(node)
        self.nodeList.sort(key= lambda node: node.cost)

    def getType(self):
        return type(self).__name__
        
    def getNextNode(self):
        returnNode = self.nodeList[0]
        self.nodeList.remove(returnNode)
        return returnNode

    def euclidianDistance(self, pointA, pointB):
        return np.sqrt( pow(abs(pointA[0] - pointB[0]) + abs( pointA[1] - pointB[1]),2))

    def calculateCost(self,newNode):
        return self.euclidianDistance(newNode.coordinates, self.goalNode.coordinates) + newNode.depth 