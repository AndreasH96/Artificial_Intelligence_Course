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
resultData= {"GreedyAgent":[], "GreedyAgentImproved":[],"DepthFirstAgent":[],"BreadthFirstAgent":[],"RandomAgent":[]}

def runGame(game):
    game.start()
    #game.printResultingState()
    return game.getResultData()
agents=[GreedyAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None),GreedyAgentImproved(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None), 
 DepthFirstAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None),BreadthFirstAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None),
 RandomAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None) ]
for agent in agents:
    for x in range(1):

        pokerGame = PokerGame(agent)
        resultData[type(agent).__name__].append(runGame(pokerGame))
   
    #pokerGame.start()
    #pokerGame.printResultingState()
    #resultData = pokerGame.getResultData()
    #print(resultData)
#print(Agent.amountOfNodesExtended)
#print(pokerGame.end_state_.nn_current_hand)
resultdf = pandas.DataFrame(resultData["GreedyAgent"])
#resultMatrix = resultdf.values()
print(np.matrix([each.values() for each in resultData]))
#print(resultMatrix)
