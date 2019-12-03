import numpy as np
import math
import heapq
from Node import Node

class SearchAgent:
    def __init__(self, searchMap= None, startPosition= None, goalPosition= None):
        self.nodeList = []
        if startPosition != None:
            self.startNode = Node(parent = 0, nodeCoordinates = startPosition, cost= 0 ,depth = 0)
        if goalPosition != None:
            self.goalNode = Node(parent = 0, nodeCoordinates = goalPosition, cost= 0 , depth = 0)
        self.searchMap = searchMap
        self.path = [[],[]]
        self.amountOfNodesExpanded = 0
        self.returnToPreviousAllowed = False

    def addNode(self,node):
        pass
    def getNextNode(self):
        pass
    def calculateCost(self,newNode):
        pass
    def getType(self):
        return None
    def getNeighbors(self,currentNode):
        neighbors= []
        neigborVectors = np.array([[1,0],[0,1],[-1,0],[0,-1]])
        for neigborCoordinates in neigborVectors + np.array(currentNode.coordinates):
           if not np.any(np.isin(neigborCoordinates , [-1,len(self.searchMap[0])])):
                newNode = Node (parent = currentNode,
                        nodeCoordinates= list(neigborCoordinates),
                        cost = 0, depth = currentNode.depth + 1 )

                newNode.cost = self.calculateCost(newNode)
                positionValue = self.searchMap[tuple(neigborCoordinates)]
                
                if (positionValue > newNode.cost and self.returnToPreviousAllowed) or positionValue in [-3,0]:
                    neighbors.append(newNode)
        return neighbors
                    
    def calculatePath(self):
        currentNode = self.goalNode
        while currentNode.coordinates is not self.startNode.coordinates:
            #Plotting function inverts the path, so give inverted 
            self.path[1].append(currentNode.coordinates[0]) 
            self.path[0].append(currentNode.coordinates[1])
            currentNode = currentNode.parent

    def search(self):
        self.addNode(self.startNode)
        while self.nodeList:
            currentNode = self.getNextNode()
            if currentNode.coordinates == self.goalNode.coordinates:
                self.goalNode.parent = currentNode
                self.calculatePath()
                break

            for nextNode in self.getNeighbors(currentNode):

                if(self.searchMap[nextNode.coordinates[0]][nextNode.coordinates[1]] >= 0):
                    self.searchMap[nextNode.coordinates[0]][nextNode.coordinates[1]] = nextNode.depth
                self.addNode(nextNode)
                self.amountOfNodesExpanded += 1

        return {"AgentType":self.getType(), "Map": self.searchMap, "Path":  self.path,  "PathLenght" : len(self.path[0]), "Expanded" : self.amountOfNodesExpanded} 

