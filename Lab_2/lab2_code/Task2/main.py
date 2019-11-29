import PokerGame
import poker_environment
from RandomAgent import RandomAgent
import poker_game_example
from poker_game_example import PokerPlayer, GameState
"""
Game flow:
Two agents will keep playing until one of them lose 100 coins or more.
"""

MAX_HANDS = 4
INIT_AGENT_STACK = 400

# initialize 2 agents and a game_state
agent = PokerPlayer(current_hand_=None, stack_=INIT_AGENT_STACK, action_=None, action_value_=None)
opponent = PokerPlayer(current_hand_=None, stack_=INIT_AGENT_STACK, action_=None, action_value_=None)


init_state = GameState(nn_current_hand_=0,
                       nn_current_bidding_=0,
                       phase_ = 'INIT_DEALING',
                       pot_=0,
                       acting_agent_=None,
                       agent_=agent,
                       opponent_=opponent,
                       )


game_state_queue = []
game_on = True
round_init = True

while game_on:

    if round_init:
        round_init = False
        states_ = get_next_states(init_state)
        game_state_queue.extend(states_[:])
    else:

        # just an example: only expanding the last return node
        states_ = get_next_states(states_[-1])
        game_state_queue.extend(states_[:])

        for _state_ in states_:
            if _state_.phase == 'SHOWDOWN' and (_state_.opponent.stack <= 300 or _state_.agent.stack <= 300): #or _state_.MAX_HANDS >= 4):
                    end_state_ = _state_
                    game_on = False


"""
Printing game flow & info
"""


state__ = end_state_
nn_level = 0

print('------------ print game info ---------------')
print('nn_states_total', len(game_state_queue))

while state__.parent_state != None:
    nn_level += 1
    print(nn_level)
    state__.print_state_info()
    state__ = state__.parent_state

print(nn_level)


"""
Perform searches
"""



