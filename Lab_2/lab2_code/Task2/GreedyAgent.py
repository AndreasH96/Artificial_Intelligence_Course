import poker_environment as environment
from poker_environment import AGENT_ACTIONS, BETTING_ACTIONS
import copy
from poker_game_example import PokerPlayer, GameState
import PokerGame
import numpy as np


class GreedyAgent(PokerPlayer):
    def __init__(self, current_hand=None, stack=300, action=None, action_value=None):
        super().__init__(current_hand_= current_hand, stack_=300, action_=action , action_value_=action_value)
        self.amountOfNodesExtended = 0

    def evaluateStates(self,states):
        optimalAction = states[0]
        for state in states:
            if state.agent.current_hand_strength > state.opponent.current_hand_strength:
                if state.agent.action == "BET25" and state.agent.stack > 25:
                    optimalAction = state
            

        nextStates = PokerGame.get_next_states(states[:])
        self.amountOfNodesExtended += 1

        return nextStates