import numpy as np
import math
import heapq

# Priority Queue based on heapq
class PriorityQueue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0
    def add(self, item, priority):
        heapq.heappush(self.elements,(priority,item))
    def remove(self):
        return heapq.heappop(self.elements)[1]

# An example of search algorithm
# modify it and implment the missing part
def search(map, start, goal, ...):

    # cost moving to another cell
    moving_cost = 1

    # open list
    frontier = PriorityQueue()
    # add starting cell to open list
    frontier.add(start, 0)

    # path taken
    came_from = {}

    # expanded list with cost value for each cell
    cost = {}

    # init. starting node
    start.parent = None
    start.g = 0

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
