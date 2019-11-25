import copy
import numpy as np
from AStarAgent import AStarAgent
from BreadthFirstAgent import BreadthFirstAgent
from DepthFirstAgent import DepthFirstAgent
from RandomAgent import RandomAgent
from AStarAgentEuclidean import AStarAgentEuclidean
from GreedySearch import GreedySearchAgent
from path_planning import plotMap, generateMap2d, generateMap2d_obstacle

searchMap = generateMap2d([100,100])
searchMapCopy = copy.copy(searchMap)
startNodeMask = np.where(searchMap == -2)
startNode = [startNodeMask[0][0],startNodeMask[1][0]]

goalNodeMask = np.where(searchMap == -3)
goalNode = [goalNodeMask[0][0],goalNodeMask[1][0]]

  # Assign RGB Val for starting point and ending point

print("Goal: %s" %goalNode)
print("Start: %s"%startNode)
greedyAgent = GreedySearchAgent(searchMap = searchMap, startPosition = startNode, goalPosition = goalNode)
resultsManhattan = greedyAgent.search()

euclideanAgent = AStarAgent(searchMap = searchMapCopy, startPosition = startNode, goalPosition = goalNode)
resultsEuclidean = euclideanAgent.search()

print("Nodes expanded: Greedy: {}     A*: {}".format(resultsManhattan["Expanded"], resultsEuclidean["Expanded"]))
print("Pathlength: Greedy: {}     A*: {}".format(resultsManhattan["PathLenght"], resultsEuclidean["PathLenght"]))
plotMap(resultsManhattan["Map"],resultsManhattan["Path"],greedyAgent.description)
plotMap(resultsEuclidean["Map"],resultsEuclidean["Path"],euclideanAgent.description)
