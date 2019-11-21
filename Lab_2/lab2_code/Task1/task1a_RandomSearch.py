import numpy as np
import math
import heapq
from PriorityQueue import PriorityQueue
from Node import Node
class RandomSearch:
    def __init__(self):
        # cost moving to another cell
        self.moving_cost = 1

        self.description = "Random Search Algorithm"

    # An example of search algorithm
    # modify it and implment the missing part
    def search(self,map, start, goal):
        # path taken
        came_from = {}
        # open list
        frontier = PriorityQueue()
        # add starting cell to open list
        frontier.add(item = start,priority= 0)

        
        # expanded list with cost value for each cell
        cost = {}

        # init. starting node
        start.parent = None
        start.g = 0

        def get_neighbors(currentNode):
            currentNodeX = currentNode.coordinates["x"]
            currentNodeY = currentNode.coordinates["y"]
            neighbours= []
            for adjacentNodeIndex in range(4):
                if [currentNodeX,currentNodeY] not in came_from:
                    neighbours.append([currentNodeX,currentNodeY])
                    #neighbours.append(came_from[came_from.index([currentNodeX,currentNodeY])])
            return neighbours


        def cost_function(nextCell):
            #Is the random search supposed to have random cost?
            pass

        # if there is still nodes to open
        while not frontier.isEmpty():
            current = frontier.remove()

            # check if the goal is reached
            if current == goal:
                break

            # for each neighbour of the current cell
            # Implement get_neighbors function (return nodes to expand next)
            # (make sure you avoid repetitions!)
            for next in get_neighbors(current):

                # compute cost to reach next cell
                # Implement cost function
                cost = cost_function()

                # add next cell to open list
                frontier.add(next, cost)
                # add to path
                came_from[next] = current

        return came_from, cost

