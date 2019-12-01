import poker_environment as environment
from poker_environment import AGENT_ACTIONS, BETTING_ACTIONS
import copy
from poker_game_example import PokerPlayer, GameState
import PokerGame
import numpy as np


class GreedyAgentImproved(PokerPlayer):
    def __init__(self, current_hand=None, stack=300, action=None, action_value=None):
        super().__init__(current_hand_= current_hand, stack_=400, action_=action , action_value_=action_value)
        self.amountOfNodesExpanded = 0

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
                        self.amountOfNodesExpanded += 1
                        #print(childState.agent.stack - childState.opponent.stack)
                        # Abandon expansion of branch more than 4 hands are dealt
                        if childState.nn_current_hand > 4 :
                            break
                        # If branch still interesting, check if current state is winning state,
                        # also check that the current state is a showdown.
                        elif (childState.agent.stack - childState.opponent.stack) >= 100 and childState.phase == "SHOWDOWN" :
                            winningStates.append(childState)
                            doneWithStateChild = True
                            print("FOUND WIN IN {} hands".format(childState.nn_current_hand))
                            break
                        # If current state is not a winning state but still interesting, 
                        # add the states child states to the list of states to check
                        childStates.extend(PokerGame.get_next_states(childState)[:])

                        childStates.sort(key= lambda state: state.nn_current_hand, reverse = True)   
                        # Improved Greedy Search with this heuristic, also sorts the list according to the amount of 
                        childStates.sort(key= lambda state: state.agent.stack - state.opponent.stack, reverse =True)

        winningStates.sort(key= lambda state: state.nn_current_hand)
        print("Hands required: {} ".format(winningStates[0].nn_current_hand))
        
        return [winningStates[0]]