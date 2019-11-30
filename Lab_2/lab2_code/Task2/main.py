from PokerGame import PokerGame
import poker_environment
import poker_game_example
from poker_game_example import PokerPlayer, GameState
import time

from RandomAgent import RandomAgent
from DepthFirstAgent import DepthFirstAgent
from GreedyAgent import GreedyAgent
"""
Game flow:
Two agents will keep playing until one of them lose 100 coins or more.
"""
INIT_AGENT_STACK = 400
randomAgent = GreedyAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None)
#startTime = time.time()
pokerGame = PokerGame(randomAgent)
pokerGame.start()
pokerGame.printResultingState()
#print("Time required: {}".format(time.time() - startTime))
print(randomAgent.amountOfNodesExtended)
