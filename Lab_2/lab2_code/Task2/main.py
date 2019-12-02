from PokerGame import PokerGame
import poker_environment
import poker_game_example
from poker_game_example import PokerPlayer, GameState
import time

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
GreedyData = []
GreedyImprovedData = []
DepthFirstData = []
BreadthFirstData = []

Agent = GreedyAgentImproved(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None)
pokerGame = PokerGame(Agent)
pokerGame.start()
pokerGame.printResultingState()
resultData = pokerGame.getResultData()
print(resultData)
#print(Agent.amountOfNodesExtended)
#print(pokerGame.end_state_.nn_current_hand)

