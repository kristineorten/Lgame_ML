import random
import numpy as np
from Lpiece import Lpiece
from Npiece import Npiece
from Lgame import Lgame

# Test gameplay visuals
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

print("Illegal n-move")
new_move = np.array([[0,3],[0,2],[1,2],[2,2]])
n_pos = np.array([[0,0],[3,0]])
print(player1.move(new_move,n_pos))
game.print_unicode()

print("Resetting the game")
print(game.reset())
game.print_unicode()


# Training the AI

def increase_turn(turn):
    return (turn+1) % 2

def find_next_states(game,current_state,l_all_pos,n_all_pos,symbol):
    """
    Params:
        current_state (numpy.ndarray): state matrix
        l_all_pos (list): all l positions (x,y-coordinates)
        n_all_pos (list): all n positions (x,y-coordinates)
        opponents_symbol (int)
    """
    next_states = []
    
    # Finding the position of the opponent and the neutral pieces
    old_l_pos,_ = state_to_pos(current_state,symbol)


    # Finding the position of the opponent and the neutral pieces
    opponents_symbol = 1
    if (symbol-1) == 0:
        opponents_symbol = 2
    l2_pos,old_n_pos = state_to_pos(current_state,opponents_symbol)
    l2_pos = l2_pos.tolist()
    old_n_pos = old_n_pos.tolist()

    # Finding possible new positions for the L-piece
    for l1_pos in l_all_pos:
        if (str(l1_pos) != str(old_l_pos)):

            legal_l_pos = True
            for pos in l1_pos:
                pos_str = str(pos)
                if (pos_str in str(l2_pos)) or (pos_str in str(old_n_pos)):
                    # The position is occupied
                    legal_l_pos = False
            if legal_l_pos:

                # Finidng possible new positions for the neutral pieces
                for n1_pos in n_all_pos:
                    if (str(n1_pos) not in str(l1_pos)) and (str(n1_pos) not in str(l2_pos)):

                        for n2_pos in n_all_pos:
                            if (str(n2_pos) not in str(l1_pos)) and (str(n2_pos) not in str(l2_pos)):

                                # One or both n's must be equal to old state
                                if (n1_pos != n2_pos) and (str(n1_pos) in str(old_n_pos) or str(n2_pos) in str(old_n_pos)):

                                    # Making the state
                                    state = np.zeros(current_state.shape)
                                    positions = [l1_pos,l2_pos,[n1_pos],[n2_pos]]

                                    for i in range(len(positions)):
                                        for pos in positions[i]:
                                            pos_x,pos_y = pos
                                            state[pos_x,pos_y] = min(i+1,len(positions)-1)

                                    state_id = game.state_to_id(state) #TODO possible to remove?

                                    # Adding to list
                                    if (state_id not in next_states):
                                        next_states.append(state_id)
    return next_states

# Initialize variables
i = 0
turn = 0
state, reward, termination, msgs = game.reset()
game.print_unicode() # For debug purposes

# Read in all states
with open("positions.txt") as file:
    all_state_ids = [line.strip() for line in file]
print(len(all_state_ids))

next_state_ids = find_next_states(game,id_to_state(state),game.l_all_pos,game.n_all_pos,turn+1)
print(len(next_state_ids))

# Initialize Q-table
Q = np.random.rand(len(all_state_ids),len(next_state_ids))

# Note "states" is here state_ids
while(not termination and i < 5): #TODO
    # Player 1
    # Finding l-piece move and neutral move
    l_action,n_action = policy_epsilon(state,all_state_ids,next_state_ids,Q,epsilon,turn+1)

    #print("l-action:",l_action)
    #print("n-action:",n_action) #n_pos = np.array([[3,3],[1,1]])

    new_state, reward, termination, msgs = player1.move(l_action,n_action)

    # Update Q-table (note: fix for rotated states)
    """
    Q[state,action] = Q[state,action] \
        + alpha*(reward + gamma*max(Q[new_state]) - Q[state,action])
    """

    state = new_state

    turn = increase_turn(turn)
    next_state_ids = find_next_states(game,id_to_state(state),game.l_all_pos,game.n_all_pos,increase_turn(turn)+1)

    # Player 2
    # Finding a random l-piece move
    possible_l_actions = game._find_available_l_pos(player2.to_symbol()) #TODO change this
    l_index = random.randint(0, len(possible_l_actions)-1)
    l_action = possible_l_actions[l_index]

    # Move n 50% of the time
    n_action = None
    if random.choice([0, 1]):
        # Finding a neutral move
        possible_n_actions = game._find_available_n_pos() #TODO change this bc _ should be private
        n_index = random.randint(0, len(possible_n_actions)-1)
        n_action = possible_n_actions[n_index]

    new_state, reward, termination, msgs = player2.move(l_action,n_action)

    if reward == 100:
        #Update Q_table with -100 because L1 lost
        pass
    elif reward == -100:
        #Update Q_table with 100 because L1 won
        pass

    game.print_unicode()
    i += 1
    turn = increase_turn(turn)
