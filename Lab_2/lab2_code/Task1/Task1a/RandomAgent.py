import numpy as np
import math
import heapq
from Node import Node

class RandomAgent:
    def __init__(self, searchMap, startPosition, goalPosition):
        self.description = "Breadth First Search Algorithm"
        self.nodeQueue = PriorityQueue()
        self.startNode = Node(parent = 0, nodeCoordinates = startPosition, cost= 0)
        self.goalNode = Node(parent = 0, nodeCoordinates = goalPosition, cost= 0)
        self.searchMap = searchMap
        self.path = [[],[]]
        self.amountOfNodesExpanded = 0
    def addNode(self,node):
        self.nodeQueue.add(node)

    def calculateCost(self,nodeCoordinates):
        return np.random.randint(1,5)
    
    def getNeighbors(self,currentNode):
        currentNodeX = currentNode.coordinates[0]
        currentNodeY = currentNode.coordinates[1]
        neighbours= []
        for exponent in range (2):
            addition = pow(-1,exponent)
            if currentNodeX + addition not in {-1,60}:
                if self.searchMap[currentNodeX + addition][currentNodeY] not in {-1,1}:

                        neighbours.append(Node(parent =currentNode,
                            nodeCoordinates=[currentNodeX + addition, currentNodeY ],
                            cost = self.calculateCost([currentNodeX + addition, currentNodeY ])))

            if currentNodeY + addition not in {-1,60}:
                if self.searchMap[currentNodeX ][currentNodeY + addition] not in {-1,1}: 

                    neighbours.append(Node(parent =currentNode,
                            nodeCoordinates=[currentNodeX, currentNodeY + addition ],
                            cost = self.calculateCost([currentNodeX, currentNodeY + addition  ])))
                            
        return neighbours
                    
    def calculatePath(self):
        currentNode = self.goalNode
        while currentNode.coordinates is not self.startNode.coordinates:
            #Plotting function inverts the path, so give inverted coordinates
            self.path[1].append(currentNode.coordinates[0]) 
            self.path[0].append(currentNode.coordinates[1])
            currentNode = currentNode.parent

    def search(self):
        self.nodeQueue.add(self.startNode)

        while not self.nodeQueue.isEmpty():
            currentNode = self.nodeQueue.remove()
            if currentNode.coordinates == self.goalNode.coordinates:
                self.goalNode.parent = currentNode
                self.calculatePath()
                break

            for nextNode in self.getNeighbors(currentNode):

                if(self.searchMap[nextNode.coordinates[0]][nextNode.coordinates[1]] == 0):
                    self.searchMap[nextNode.coordinates[0]][nextNode.coordinates[1]] = 1
                    
                self.nodeQueue.add(nextNode)
                self.amountOfNodesExpanded += 1

        return {"Map" : self.searchMap, "Path":  self.path,  "PathLenght" : len(self.path[0]), "Expanded" : self.amountOfNodesExpanded} 


# Priority Queue 
class PriorityQueue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0

    def updateNode(self,oldNode, newNode):
        self.elements.remove(oldNode)
        self.add(newNode)

    def add(self, node):
        self.elements.append(node)
        self.elements.sort(key= lambda node: node.cost)


    def remove(self):
        returnNode = self.elements[0]
        self.elements.remove(returnNode)
        return returnNode
