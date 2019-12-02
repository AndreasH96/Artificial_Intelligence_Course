from copy import copy
import numpy as np
from AStarAgentManhattan import AStarAgentManhattan
from BreadthFirstAgent import BreadthFirstAgent
from DepthFirstAgent import DepthFirstAgent
from RandomAgent import RandomAgent
from AStarAgentEuclidean import AStarAgentEuclidean
from GreedyAgentManhattan import GreedyAgentManhattan
from path_planning import plotMap, generateMap2d, generateMap2d_obstacle
from AStarAgentCustom import AStarAgentCustom
import matplotlib.pyplot as plt

searchMap , info= generateMap2d_obstacle([100,100])
print(info)
searchMapCopy = copy(searchMap)
startNodeMask = np.where(searchMap == -2)
startNode = [startNodeMask[0][0],startNodeMask[1][0]]

goalNodeMask = np.where(searchMap == -3)
goalNode = [goalNodeMask[0][0],goalNodeMask[1][0]]

  # Assign RGB Val for starting point and ending point

print("Goal: %s" %goalNode)
print("Start: %s"%startNode)
agent = AStarAgentCustom(searchMap = searchMap, startPosition = startNode, goalPosition = goalNode, boardInfo = info)
results = agent.search()

euclideanAgent = BreadthFirstAgent(searchMap = searchMapCopy, startPosition = startNode, goalPosition = goalNode)
resultsEuclidean = euclideanAgent.search() 

print("Nodes expanded: Custom: {}   A*: {}  ".format(results["Expanded"], resultsEuclidean["Expanded"]))
print("Pathlength: Custom: {}    A*: {} ".format(results["PathLenght"], resultsEuclidean["PathLenght"]))

#plotMap(results["Map"],results["Path"],"Type: {}, Nodes: {}, PathL: {}".format(agent.description,results["Expanded"],results["PathLenght"]))
#plotMap(resultsEuclidean["Map"],resultsEuclidean["Path"],"Type: {}, Nodes: {}, PathL: {}".format(euclideanAgent.description,resultsEuclidean["Expanded"],resultsEuclidean["PathLenght"]))
#plt.show()


