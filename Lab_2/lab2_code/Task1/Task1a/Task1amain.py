from copy import copy
import numpy as np
from AStarAgentManhattan import AStarAgentManhattan
from AStarAgentEuclidean import AStarAgentEuclidean

from BreadthFirstAgent import BreadthFirstAgent
from DepthFirstAgent import DepthFirstAgent
from RandomAgent import RandomAgent

from GreedyAgentManhattan import GreedyAgentManhattan
from GreedyAgentEuclidean import GreedyAgentEuclidean

from path_planning import plotMap, generateMap2d
import pandas

agents = [AStarAgentManhattan(), AStarAgentEuclidean(), GreedyAgentManhattan(), GreedyAgentEuclidean(), BreadthFirstAgent(), DepthFirstAgent(), RandomAgent()]
resultData = {"AStarAgentManhattan":[],"AStarAgentEuclidean":[],"GreedyAgentManhattan":[], "GreedyAgentEuclidean":[],"BreadthFirstAgent":[],"DepthFirstAgent":[],"RandomAgent":[]}
analysedResultData = []
def analyseResults(resultList):
    analysedResults = {"AgentType":resultList[0]["AgentType"], "PathLenght":0 , "Expanded":0 }
    for result in resultList:
        for key in result.keys():
            if key != "AgentType" and key in analysedResults.keys():
                analysedResults[key] += result[key]
  
    for key in analysedResults.keys():
        if key != "AgentType" and key != "Wins":
            analysedResults[key] = analysedResults.get(key)/len(resultList)
    return analysedResults

for roundIndex in range (10):
    searchMap = generateMap2d([100,100])
    for agent in agents: 
        searchMapCopy = copy(searchMap)
        startNodeMask = np.where(searchMap == -2)
        startNode = [startNodeMask[0][0],startNodeMask[1][0]]
        goalNodeMask = np.where(searchMap == -3)
        goalNode = [goalNodeMask[0][0],goalNodeMask[1][0]]    
        agent.__init__(searchMap= searchMapCopy, startPosition= startNode, goalPosition= goalNode)
        agentResults = agent.search()
        resultData[type(agent).__name__].append(agentResults)

for agentKey in resultData.keys():
    analysedResultData.append(analyseResults(resultData[agentKey]))

print(pandas.DataFrame(analysedResultData))


''' 
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
 '''