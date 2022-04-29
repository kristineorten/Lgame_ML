#import random
import numpy as np
from functions import id_to_state, state_to_pos
#from Lpiece import Lpiece
#from Npiece import Npiece
#from Lgame import Lgame

def policy_epsilon(state_id,all_state_ids,next_state_ids,Q,eps,symbol,game):
    """ TODO
    Params:

    Returns
        numpy.ndarray
    """
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
        old_state = np.rot90(old_state)
        state_id = game.state_to_id(old_state)

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

    print("Old state:")
    game.print_unicode(old_state);
    print("New state:")
    game.print_unicode(new_state);
    if (new_state == old_state).all():
        print("OPS") #TODO: remove old_state? must move the piece

    _,old_n_pos = state_to_pos(old_state,symbol,[3,3])
    l_action,new_n_pos = state_to_pos(new_state,symbol,[3,3])

    n_action = np.zeros((2,2)).astype('int')

    p1, p2 = new_n_pos
    p1_old, p2_old = old_n_pos

    #print("old n",old_n_pos)
    #print("new n",new_n_pos)

    if (p1 == p1_old).all():
        n_action[0] = p2_old
        n_action[1] = p2
    elif (p1 == p2_old).all():
        n_action[0] = p1_old
        n_action[1] = p2

    elif (p2 == p1_old).all():
        n_action[0] = p2_old
        n_action[1] = p1
    else: #p2 == p2_old:
        n_action[0] = p1_old
        n_action[1] = p1

    return l_action,n_action
