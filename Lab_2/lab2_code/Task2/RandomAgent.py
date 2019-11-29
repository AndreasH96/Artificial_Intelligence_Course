import poker_environment as environment
from poker_environment import AGENT_ACTIONS, BETTING_ACTIONS
import copy
from poker_game_example import PokerPlayer, GameState, get_next_states

class RandomAgent(PokerPlayer):
    def __init__(self, current_hand_=None, stack_=300, action_=None, action_value_=None):
        super.__init__(self, current_hand_=None, stack_=300, action_=None, action_value_=None)
        