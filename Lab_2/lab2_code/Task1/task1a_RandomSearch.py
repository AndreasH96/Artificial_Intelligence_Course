import numpy as np
import math
import heapq
from PriorityQueue import PriorityQueue
from Node import Node
from pathPlotter import ScatterPlotter
class RandomSearch:
    def __init__(self):
        # cost moving to another cell
        self.moving_cost = 1
        self.count = 0
        self.description = "Random Search Algorithm"

    # An example of search algorithm
    # modify it and implment the missing part
    def search(self,map, start, goal):
        # path taken
        
        came_from = {}
        path = [[],[]]
        # open list
        frontier = PriorityQueue()
        # add starting cell to open list
        frontier.add(item = start,priority= 0)

        # expanded list with cost value for each cell
        cost = {}
        plotter = ScatterPlotter()
        #plotter.setMap(map)
        def get_neighbors(currentNode):
            currentNodeX = currentNode[0]
            currentNodeY = currentNode[1]
            neighbours= []
            for exponent in range (2):
                addition = pow(-1,exponent)
                if ([currentNodeX + addition , currentNodeY] not in came_from.values()) and currentNodeX + addition not in {-1,60}:
                    if map[currentNodeX + addition][currentNodeY] is not (-1):
                        neighbours.append([currentNodeX + addition, currentNodeY ])
            
                if ([currentNodeX , currentNodeY + addition] not in came_from.values())  and currentNodeY + addition not in {-1,60}:
                    if map[currentNodeX][currentNodeY + addition] is not (-1):
                        neighbours.append([currentNodeX, currentNodeY + addition])
            print("Current pos: x:%s, y%s mapVal: %s"%(currentNodeX,currentNodeY, map[currentNodeX][currentNodeY]))
            return neighbours

        #def calcManhattanDistance()
        def cost_function(position):
            #Is the random search supposed to have random cost?

            randCost = np.random.randint(1,3)
            return randCost

        # if there is still nodes to open
        while not frontier.isEmpty():
            current = frontier.remove()

            # check if the goal is reached
            if current == goal:
                print(start)
                print(current)
                break

            # for each neighbour of the current cell
            # Implement get_neighbors function (return nodes to expand next)
            # (make sure you avoid repetitions!)
            neighborsWithCosts =[]
            for next in get_neighbors(current):
                if map[next[0]][next[1]] != (-1):
                    # compute cost to reach next cell
                    # Implement cost function
                    cost = cost_function(next)
                    if(map[next[0]][next[1]] == 0):
                        map[next[0]][next[1]] = 1
                    frontier.add(next, cost)

                # add to path
                    came_from[str(next)] = current
                
                    #path[1].append(current[0])
                    #path[0].append(current[1])
        
        return map, path, cost

        
