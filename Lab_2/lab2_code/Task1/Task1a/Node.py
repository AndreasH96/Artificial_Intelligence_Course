class Node:
    def __init__(self, parent, nodeCoordinates, cost ,depth= 0):
        self.parent = parent
        self.cost = cost
        self.depth = depth
        self.coordinates= [nodeCoordinates[0],nodeCoordinates[1]]
