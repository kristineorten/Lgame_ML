import numpy as np
from Lpiece import Lpiece
from Npiece import Npiece
from Lgame import Lgame


# Test gameplay
print("Setting up the game")
game = Lgame()
player1, player2 = game.get_players()
game.print_unicode()

print("Attempting an illegal move")
new_move = np.array([[1,0],[2,0],[3,0],[3,1]])
print(player1.move(new_move))
game.print_unicode()

print("Moving the L-piece")
new_move = np.array([[0,2],[1,2],[2,2],[2,3]])
print(player1.move(new_move))
game.print_unicode()

print("Moving both the L- and N-pieces")
new_move = np.array([[2,0],[3,0],[3,1],[3,2]])
n_pos = np.array([[3,3],[1,1]])
print(player2.move(new_move,n_pos))
game.print_unicode()

print("Resetting the game")
print(game.reset())
game.print_unicode()


# Read in all states
with open("positions.txt") as file:
    all_state_ids = [line.strip() for line in file]
print(len(all_state_ids))

#state, reward, termination, msgs



# TODO
# Tests
def increase_turn(turn):
    return (turn+1) % 2

i = 0
turn = 0

state, reward, termination, msgs = game.reset()
game.print_unicode()

next_state_ids = find_next_states(game,id_to_state(state),game.l_all_pos,game.n_all_pos,turn+1)
#print("next_state_ids",next_state_ids,len(next_state_ids))
Q = np.random.rand(len(all_state_ids),len(next_state_ids)) #l2 and 1-2 n same, l1 and 0-1 n changed

# Note "states" is here state_ids
while(not termination and i < 5): #TODO
    # Player 1
    # Finding l-piece move and neutral move
    l_action,n_action = policy_epsilon(state,all_state_ids,next_state_ids,Q,epsilon,turn+1)

    #print("l-action:",l_action)
    #print("n-action:",n_action) #n_pos = np.array([[3,3],[1,1]])

    new_state, reward, termination, msgs = player1.move(l_action,n_action) #n prev action

    # Update Q-table (note: fix for rotated states)
    """
    Q[state,action] = Q[state,action] \
        + alpha*(reward + gamma*max(Q[new_state]) - Q[state,action])
    """

    state = new_state

    turn = increase_turn(turn)
    next_state_ids = find_next_states(game,id_to_state(state),game.l_all_pos,game.n_all_pos,increase_turn(turn)+1)
    #print("next_state_ids",next_state_ids,len(next_state_ids))
    # Player 2
    # Finding l-piece move and neutral move
    # DO NOT update Q-table

    game.print_unicode()
    i += 1
    turn = increase_turn(turn)

    #next_state_ids = find_next_states(game,id_to_state(state),game.l_all_pos,game.n_all_pos,increase_turn(turn)+1)
    #print("next_state_ids",next_state_ids,len(next_state_ids))
