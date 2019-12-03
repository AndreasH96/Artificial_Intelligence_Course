import numpy as np
import math
import heapq
from Node import Node
from SearchAgent import SearchAgent
class GreedyAgentManhattan(SearchAgent):

    def __init__(self, searchMap= None, startPosition= None, goalPosition= None):
        super().__init__(searchMap, startPosition, goalPosition)
        self.description = "Greedy Manhattan"
        self.returnToPreviousAllowed = False
    def getType(self):
        return type(self).__name__
    def addNode(self,node):
        self.nodeList.append(node)
        self.nodeList.sort(key= lambda node: node.cost)

    def getNextNode(self):
        returnNode = self.nodeList[0]
        self.nodeList.remove(returnNode)
        return returnNode

    def manhattanDistance(self, pointA, pointB):
        return abs(pointA[0] - pointB[0]) + abs( pointA[1] - pointB[1])

    def calculateCost(self,newNode):
        return self.manhattanDistance(newNode.coordinates, self.goalNode.coordinates) 
    

