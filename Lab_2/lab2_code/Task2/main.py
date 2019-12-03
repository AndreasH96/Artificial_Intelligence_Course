from PokerGame import PokerGame
import poker_environment
import poker_game_example
from poker_game_example import PokerPlayer, GameState
import pandas
import numpy as np
from RandomAgent import RandomAgent
from DepthFirstAgent import DepthFirstAgent
from GreedyAgent import GreedyAgent
from GreedyAgentImproved import GreedyAgentImproved
from BreadthFirstAgent import BreadthFirstAgent

"""
Game flow:
Two agents will keep playing until one of them lose 100 coins or more.
"""
INIT_AGENT_STACK = 400
resultData = []
agents=[GreedyAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None),GreedyAgentImproved(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None), 
 DepthFirstAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None),BreadthFirstAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None),
 RandomAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None) ]

def analyseResults(resultList):
    analysedResults = {"AgentType":resultList[0]["AgentType"]
        , "AgentStack":0,"OpponentStack":0 ,"PathLength":0 ,"Expanded": 0,"Wins":0, "Hands": 0}
    for result in resultList:
        for key in result.keys():
            if key != "AgentType":
                analysedResults[key] += result[key]
                
        if result["AgentStack"] > result["OpponentStack"]:
            analysedResults["Wins"] += 1

    for key in analysedResults.keys():
        if key != "AgentType" and key != "Wins":
            analysedResults[key] = analysedResults[key]/len(resultList)
    return analysedResults

def runGame(game):
    game.start()
    return game.getResultData()


for agent in agents:
    pokerResults = []
    for x in range(10):
        pokerGame = PokerGame(agent)
        pokerResults.append(runGame(pokerGame))
        
    agentResults = analyseResults(pokerResults)
    resultData.append(agentResults)
   

resultDataFrame = pandas.DataFrame(resultData)

print(resultDataFrame)