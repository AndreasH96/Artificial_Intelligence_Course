import numpy as np
import math
import heapq
from Node import Node
from SearchAgent import SearchAgent
class AStarAgentCustom(SearchAgent):

    def __init__(self, searchMap, startPosition, goalPosition, boardInfo):
        super().__init__(searchMap, startPosition, goalPosition)
        self.description = "A* Custom"
        self.boardInfo = {"TopY": boardInfo[0], "BottomY": boardInfo[1], "MiddleX": boardInfo[2]}
        self.returnToPreviousAllowed = True
        
    def addNode(self,node):
        self.nodeList.append(node)
        self.nodeList.sort(key= lambda node: node.cost)

    def getNextNode(self):
        returnNode = self.nodeList[0]
        self.nodeList.remove(returnNode)
        return returnNode

    def manhattanDistance(self, pointA, pointB):
        return abs(pointA[0] - pointB[0]) + abs( pointA[1] - pointB[1])

    def euclidianDistance(self, pointA, pointB):
        return np.sqrt( pow(abs(pointA[0] - pointB[0]) + abs( pointA[1] - pointB[1]),2))
    
    def calcObstacleCost(self, position):
        if position[0] < self.boardInfo["TopY"] and position[0] > self.boardInfo["BottomY"]:
            if position[1] < self.boardInfo["MiddleX"]:
                return (self.boardInfo["MiddleX"] - position[1]) * 100 
            return 0
        else: 
            return 0

    def calculateCost(self,newNode):
        if newNode.coordinates[1] > newNode.parent.coordinates[1]:
            return self.manhattanDistance(newNode.coordinates, self.goalNode.coordinates) + newNode.depth + self.calcObstacleCost(newNode.coordinates)
        else:
            return self.manhattanDistance(newNode.coordinates, self.goalNode.coordinates) + newNode.depth