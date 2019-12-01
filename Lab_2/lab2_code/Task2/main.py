from PokerGame import PokerGame
import poker_environment
import poker_game_example
from poker_game_example import PokerPlayer, GameState
import time

from RandomAgent import RandomAgent
from DepthFirstAgent import DepthFirstAgent
from GreedyAgent import GreedyAgent
from GreedyAgentImproved import GreedyAgentImproved
"""
Game flow:
Two agents will keep playing until one of them lose 100 coins or more.
"""
INIT_AGENT_STACK = 400
GreedyData=[]
GreedyImprovedData=[]

Agent = DepthFirstAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None)
    #startTime = time.time()
pokerGame = PokerGame(Agent)
pokerGame.start()
pokerGame.printResultingState()
print(Agent.amountOfNodesExtended)
''' for x in range(10):

    Agent = GreedyAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None)
    #startTime = time.time()
    pokerGame = PokerGame(Agent)
    pokerGame.start()
    pokerGame.printResultingState()
    GreedyData.append(pokerGame.amountOfNodesExpanded)

    Agent = GreedyAgentImproved(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None)
    #startTime = time.time()
    pokerGame = PokerGame(Agent)
    pokerGame.start()
    pokerGame.printResultingState()
    GreedyImprovedData.append(pokerGame.amountOfNodesExpanded)
    #print("Time required: {}".format(time.time() - startTime))
print("Greedy: {}\n Improved: {}".format(GreedyData, GreedyImprovedData)) '''
