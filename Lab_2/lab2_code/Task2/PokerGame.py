import poker_environment as environment
from poker_environment import AGENT_ACTIONS, BETTING_ACTIONS
import poker_game_example
from poker_game_example import PokerPlayer, GameState
from RandomAgent import RandomAgent
import copy

MAX_HANDS = 4
INIT_AGENT_STACK = 400
MAX_EXTENDED = 10000

class PokerGame():
    
    def __init__(self, agent):
        self.agent = agent
        self.opponent = PokerPlayer(current_hand_=None, stack_=INIT_AGENT_STACK, action_=None, action_value_=None)
        self.initState = GameState(nn_current_hand_=0,
                       nn_current_bidding_=0,
                       phase_ = 'INIT_DEALING',
                       pot_=0,
                       acting_agent_=None,
                       agent_=agent,
                       opponent_=self.opponent,
                       )
        self.game_state_queue = []
        self.game_on = True
        self.round_init = True
        self.end_state_ = None
        self.amountOfHandsDealed = 0
    
    def shouldEndGame(self,state):
            if state.phase == 'SHOWDOWN' and ((state.agent.stack - state.opponent.stack) >= 100  ) or self.agent.amountOfNodesExtended == MAX_EXTENDED :#or state.nn_current_hand == MAX_HANDS:
                return True
            return False
    def start(self):
        while self.game_on:

            if self.round_init:
                self.round_init = False
                states_ = get_next_states(self.initState)
                self.game_state_queue.extend(states_[:])
            else:
                #-------------- CHANGE HERE IF NEEDED ----------------#
                
                # just an example: only expanding the last return node
                #states_ = get_next_states(states_[-1])
                states_ = self.agent.evaluateStates(self.game_state_queue.pop(0)) 
                self.game_state_queue.extend(states_)
                #self.agent.amountOfNodesExtended +=1 
                for _state_ in states_:
                    if self.shouldEndGame(_state_):
                            self.end_state_ = _state_
                            self.game_on = False
                #--------------------------------------------------------
                            
                            
    def printResultingState(self):
            
        state__ = self.end_state_
        if(state__ != None):
            nn_level = 0

            print('------------ print game info ---------------')
            print('nn_states_total', len(self.game_state_queue))
            printQueue = []
            while state__.parent_state != None:
                printQueue.append(state__)
                state__ = state__.parent_state

            printQueue.reverse()
            for state in printQueue:
                nn_level += 1
                print("nn_level: {}".format(nn_level))
                state.print_state_info()
            print("Final nn_level: {}".format(nn_level))
            #self.amountOfNodesExpanded = nn_level
    # copy given state in the argument
def copy_state(game_state):
    _state = copy.copy(game_state)
    _state.agent = copy.copy(game_state.agent)
    _state.opponent = copy.copy(game_state.opponent)
    return _state

"""
successor function for generating next state(s)
"""
def get_next_states(last_state):

    if last_state.phase == 'SHOWDOWN' or last_state.acting_agent == 'opponent' or last_state.phase == 'INIT_DEALING':

        # NEW BETTING ROUND, AGENT ACT FIRST

        states = []

        for _action_ in last_state.agent.get_actions():

            _state_ = copy_state(last_state)
            _state_.acting_agent = 'agent'

            if last_state.phase == 'SHOWDOWN' or last_state.phase == 'INIT_DEALING':
                _state_.dealing_cards()
                
            if _action_ == 'CALL':

                _state_.phase = 'SHOWDOWN'
                _state_.agent.action = _action_
                _state_.agent.action_value = 5
                _state_.agent.stack -= 5
                _state_.pot += 5

                _state_.showdown()

                _state_.nn_current_hand += 1
                _state_.nn_current_bidding = 0
                _state_.pot = 0
                _state_.parent_state = last_state
                states.append(_state_)

            elif _action_ == 'FOLD':

                _state_.phase = 'SHOWDOWN'
                _state_.agent.action = _action_
                _state_.opponent.stack += _state_.pot

                _state_.nn_current_hand += 1
                _state_.nn_current_bidding = 0
                _state_.pot = 0
                _state_.parent_state = last_state
                states.append(_state_)


            elif _action_ in BETTING_ACTIONS:

                _state_.phase = 'BIDDING'
                _state_.agent.action = _action_
                _state_.agent.action_value = int(_action_[3:])
                _state_.agent.stack -= int(_action_[3:])
                _state_.pot += int(_action_[3:])

                _state_.nn_current_bidding += 1
                _state_.parent_state = last_state
                states.append(_state_)

            else:

                print('...unknown action...')
                exit()

        return states

    elif last_state.phase == 'BIDDING' and last_state.acting_agent == 'agent':

        states = []
        _state_ = copy_state(last_state)
        _state_.acting_agent = 'opponent'

        opponent_action, opponent_action_value = environment.poker_strategy_example(last_state.opponent.current_hand_type[0],
                                                                            last_state.opponent.current_hand_type[1],
                                                                            last_state.opponent.stack,
                                                                            last_state.agent.action,
                                                                            last_state.agent.action_value,
                                                                            last_state.agent.stack,
                                                                            last_state.pot,
                                                                            last_state.nn_current_bidding)

        if opponent_action =='CALL':

            _state_.phase = 'SHOWDOWN'
            _state_.opponent.action = opponent_action
            _state_.opponent.action_value = 5
            _state_.opponent.stack -= 5
            _state_.pot += 5

            _state_.showdown()

            _state_.nn_current_hand += 1
            _state_.nn_current_bidding = 0
            _state_.pot = 0
            _state_.parent_state = last_state
            states.append(_state_)

        elif opponent_action == 'FOLD':

            _state_.phase = 'SHOWDOWN'

            _state_.opponent.action = opponent_action
            _state_.agent.stack += _state_.pot

            _state_.nn_current_hand += 1
            _state_.nn_current_bidding = 0
            _state_.pot = 0
            _state_.parent_state = last_state
            states.append(_state_)

        elif opponent_action + str(opponent_action_value) in BETTING_ACTIONS:

            _state_.phase = 'BIDDING'

            _state_.opponent.action = opponent_action
            _state_.opponent.action_value = opponent_action_value
            _state_.opponent.stack -= opponent_action_value
            _state_.pot += opponent_action_value

            _state_.nn_current_bidding += 1
            _state_.parent_state = last_state
            states.append(_state_)

        else:
            print('unknown_action')
            exit()
        return states
