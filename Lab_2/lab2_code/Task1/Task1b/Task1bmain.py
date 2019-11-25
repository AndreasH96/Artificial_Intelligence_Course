import copy
import numpy as np
from AStarAgentManhattan import AStarAgentManhattan
from BreadthFirstAgent import BreadthFirstAgent
from DepthFirstAgent import DepthFirstAgent
from RandomAgent import RandomAgent
from AStarAgentEuclidean import AStarAgentEuclidean
from GreedySearchManhattan import GreedySearchManhattan
from path_planning import plotMap, generateMap2d, generateMap2d_obstacle
from AStarAgentCustom import AStarAgentCostum
searchMap , info= generateMap2d_obstacle([60,60])
print(info)
#plotMap(searchMap,[[0],[0]],"test")
searchMapCopy = copy.copy(searchMap)
startNodeMask = np.where(searchMap == -2)
startNode = [startNodeMask[0][0],startNodeMask[1][0]]

goalNodeMask = np.where(searchMap == -3)
goalNode = [goalNodeMask[0][0],goalNodeMask[1][0]]

  # Assign RGB Val for starting point and ending point

print("Goal: %s" %goalNode)
print("Start: %s"%startNode)
agent = AStarAgentCostum(searchMap = searchMap, startPosition = startNode, goalPosition = goalNode, boardInfo = info)
results = agent.search()

euclideanAgent = AStarAgentEuclidean(searchMap = searchMapCopy, startPosition = startNode, goalPosition = goalNode)
resultsEuclidean = euclideanAgent.search() 

print("Nodes expanded: Greedy: {}   A*: {}  ".format(results["Expanded"], resultsEuclidean["Expanded"]))
print("Pathlength: Greedy: {}    A*: {} ".format(results["PathLenght"], resultsEuclidean["PathLenght"]))
plotMap(results["Map"],results["Path"],agent.description)
plotMap(resultsEuclidean["Map"],resultsEuclidean["Path"],euclideanAgent.description)
