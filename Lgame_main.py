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

def id_to_state(state_id):
    i = 0
    state = np.zeros((4,4))
    for x in range(state.shape[0]):
        for y in range(state.shape[1]):
            state[x][y] = state_id[i]
            i += 1
    return state

def state_to_pos(state,l_symbol,n_symbol=None):
    if n_symbol is None:
        n_symbol = [3,4]

    l_pos = np.zeros((4,2)).astype('int')
    n_pos = np.zeros((len(n_symbol),2)).astype('int')

    i,j = [0,0]
    for x in range(state.shape[0]):
        for y in range(state.shape[1]):
            sq = np.array([x,y])

            if state[x][y] == l_symbol:
                l_pos[i] = sq
                i += 1

            elif (j < len(n_symbol)) and (state[x][y] == n_symbol[j]):
                n_pos[j] = sq
                j += 1

    return l_pos,n_pos

def policy_epsilon(state_id,all_state_ids,next_state_ids,Q,eps,symbol):
    nr_of_next_states = Q.shape[1]
    prob_rd = eps/(nr_of_next_states-1)
    probabilities = [prob_rd]*(nr_of_next_states-1)
    probabilities.append(1-eps)
    index = np.random.choice(nr_of_next_states, 1, p=probabilities)[0]
    # numbers 0 to (n-2) with prob eps (eps/(n-1) per value)
    # number (n-1) with prob (1-eps)

    state_id = state_id.replace("4","3")
    old_state = id_to_state(state_id)

    # Rotate state
    while state_id not in all_state_ids: #TODO here
        old_state = np.rotate90(old_state)
        old_id = state_to_id(old_state)

    index_max = np.argmax(Q[all_state_ids.index(state_id)])

    # "Best" action
    if index == (nr_of_next_states-1):
        new_state_id = next_state_ids[index_max]

    # Random action
    else:
        if index_max <= index:
            index += 1
        new_state_id = next_state_ids[index]

    new_state = id_to_state(new_state_id)

    print("old_state\n",old_state)
    print("new_state\n",new_state)

    _,old_n_pos = state_to_pos(old_state,symbol,[3,3])
    l_action,new_n_pos = state_to_pos(new_state,symbol,[3,3])

    old_n_pos = old_n_pos.tolist()
    new_n_pos = new_n_pos.tolist()
    n_action = np.zeros((2,2)).astype('int')

    p1, p2 = new_n_pos
    p1_old, p2_old = old_n_pos

    #print("old n",old_n_pos)
    #print("new n",new_n_pos)

    if p1 == p1_old:
        n_action[0] = p2_old
        n_action[1] = p2
    elif p1 == p2_old:
        n_action[0] = p1_old
        n_action[1] = p2

    elif p2 == p1_old:
        n_action[0] = p2_old
        n_action[1] = p1
    else: #p2 == p2_old:
        n_action[0] = p1_old
        n_action[1] = p1

    return l_action,n_action

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
