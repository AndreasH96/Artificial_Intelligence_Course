from PokerGame import PokerGame
import poker_environment
from RandomAgent import RandomAgent
import poker_game_example
from poker_game_example import PokerPlayer, GameState
"""
Game flow:
Two agents will keep playing until one of them lose 100 coins or more.
"""
INIT_AGENT_STACK = 400
randomAgent = RandomAgent(current_hand=None, stack=INIT_AGENT_STACK, action=None, action_value=None)

pokerGame = PokerGame(randomAgent)
pokerGame.start()
pokerGame.printResultingState()
