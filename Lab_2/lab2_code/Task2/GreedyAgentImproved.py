import poker_environment as environment
from poker_environment import AGENT_ACTIONS, BETTING_ACTIONS
import copy
from poker_game_example import PokerPlayer, GameState
import PokerGame
import numpy as np
from operator import attrgetter

class GreedyAgentImproved(PokerPlayer):
    def __init__(self, current_hand=None, stack=300, action=None, action_value=None):
        super().__init__(current_hand_= current_hand, stack_=400, action_=action , action_value_=action_value)
        self.amountOfNodesExtended = 0
        self.hasDepthLimit = False
        
    def evaluateState(self,stateQueue):
        stateQueue.sort(key= lambda childState: (childState.nn_current_hand, childState.opponent.stack - childState.agent.stack ))
        childStates = PokerGame.get_next_states(stateQueue.pop(0))
        return (childStates)