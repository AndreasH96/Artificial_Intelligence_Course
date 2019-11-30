import poker_environment as environment
from poker_environment import AGENT_ACTIONS, BETTING_ACTIONS
import copy
from poker_game_example import PokerPlayer, GameState
import PokerGame
import numpy as np


class GreedyAgent(PokerPlayer):
    def __init__(self, current_hand=None, stack=300, action=None, action_value=None):
        super().__init__(current_hand_= current_hand, stack_=400, action_=action , action_value_=action_value)
        self.amountOfNodesExtended = 0

    def evaluateStates(self,states):
        winningStates = []
  
        extended = []
        for state in states:
            currentState = PokerGame.copy_state(state)
            childStates=PokerGame.get_next_states(currentState)
            doneWithStateChild = False
            while not doneWithStateChild:
                for childState in childStates:
                    if childState not in extended:
                        extended.append(childState)
                        self.amountOfNodesExtended += 1
                        print(childState.agent.stack - childState.opponent.stack)
                        if (childState.agent.stack - childState.opponent.stack) >= 100 :
                            childState.phase = "SHOWDOWN"
                            winningStates.append(childState)
                            doneWithStateChild = True
                            print("FOUND WIN")
                            return [childState]
                            break
                        elif childState.nn_current_hand > 4:
                            break
                        childStates.extend(PokerGame.get_next_states(childState)[:])
                        
                        #childStates.sort(key= lambda state: state.nn_current_hand, reverse = True)   
                        childStates.sort(key= lambda state: state.agent.stack - state.opponent.stack, reverse =True)
        winningStates.sort(key= lambda state: state.nn_current_hand, reverse= True)
        
        return [winningStates[0]]