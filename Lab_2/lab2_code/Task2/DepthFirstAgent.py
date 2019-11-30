import poker_environment as environment
from poker_environment import AGENT_ACTIONS, BETTING_ACTIONS
import copy
from poker_game_example import PokerPlayer, GameState
import PokerGame
import numpy as np


class DepthFirstAgent(PokerPlayer):
    def __init__(self, current_hand=None, stack=300, action=None, action_value=None):
        super().__init__(current_hand_= current_hand, stack_=300, action_=action , action_value_=action_value)
        self.amountOfNodesExtended = 0

    def evaluateStates(self,states):
        nextStates = []
        for state in states:
            newStates = PokerGame.get_next_states(state)
            #if shouldEndGame(new)
            nextStates.append(PokerGame.get_next_states(state))
            self.amountOfNodesExtended += 1

        return nextStates