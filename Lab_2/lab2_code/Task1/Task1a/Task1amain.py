import copy
import numpy as np
from AStarAgentManhattan import AStarAgentManhattan
from AStarAgentEuclidean import AStarAgentEuclidean

from BreadthFirstAgent import BreadthFirstAgent
from DepthFirstAgent import DepthFirstAgent
from RandomAgent import RandomAgent

from GreedyAgentManhattan import GreedyAgentManhattan
from GreedyAgentEuclidean import GreedyAgentEuclidean

from path_planning import plotMap, generateMap2d

agents = [AStarAgentManhattan(), AStarAgentEuclidean(), GreedyAgentManhattan(),GreedyAgentEuclidean(), BreadthFirstAgent(), DepthFirstAgent(), RandomAgent()]

def analyseResults(resultList):
    analysedResults = {"AgentType":resultList[0]["AgentType"]
        , "AgentStack":0,"OpponentStack":0 , "Expanded": 0,"ExpandSpan":0, "Hands": 0}
    for result in resultList:
        for key in result.keys():
            if key != "AgentType":
                analysedResults[key] = (analysedResults[key] + result[key])/(resultList.index(result) + 1)
    return analysedResults

for agent in agents: 
  for roundIndex in range (10):
        


searchMap = generateMap2d([100,100])
searchMapCopy = copy.copy(searchMap)
startNodeMask = np.where(searchMap == -2)
startNode = [startNodeMask[0][0],startNodeMask[1][0]]

goalNodeMask = np.where(searchMap == -3)
goalNode = [goalNodeMask[0][0],goalNodeMask[1][0]]
  
print("Goal: %s" %goalNode)
print("Start: %s"%startNode)
greedyAgent = AStarAgentEuclidean(searchMap = searchMap, startPosition = startNode, goalPosition = goalNode)
resultsManhattan = greedyAgent.search()

# euclideanAgent = AStarAgentManhattan(searchMap = searchMapCopy, startPosition = startNode, goalPosition = goalNode)
# resultsEuclidean = euclideanAgent.search()

# print("Nodes expanded: Greedy: {}     A*: {}".format(resultsManhattan["Expanded"], resultsEuclidean["Expanded"]))
# print("Pathlength: Greedy: {}     A*: {}".format(resultsManhattan["PathLenght"], resultsEuclidean["PathLenght"]))
plotMap(resultsManhattan["Map"],resultsManhattan["Path"],greedyAgent.description)
#plotMap(resultsEuclidean["Map"],resultsEuclidean["Path"],euclideanAgent.description)
