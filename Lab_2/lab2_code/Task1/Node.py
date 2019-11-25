class Node:
    def __init__(self, parent, nodeCoordinates, cost):
        self.parent = parent
        self.cost = cost
        self.coordinates= [nodeCoordinates[0],nodeCoordinates[1]]
