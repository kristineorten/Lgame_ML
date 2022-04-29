import numpy as np
from Lpiece import Lpiece
from Npiece import Npiece
from Lgame import Lgame

game = Lgame()
player1, player2 = game.get_players()

def test_init():
    init_state = np.array([
        [3,1,1,0],
        [0,2,1,0],
        [0,2,1,0],
        [0,2,2,3]])
    init_state_id = game.state_to_id(init_state)

    state_id = game.state_to_id()

    assert init_state_id == state_id

def test_illegal_l_move():
    old_state_id = game.state_to_id()

    new_move = np.array([[1,0],[2,0],[3,0],[3,1]])
    state_id, reward, termination, msgs = player1.move(new_move)

    assert state_id == old_state_id
    assert reward == -1
    assert termination == False
    assert msgs == "Illegal move"

def test_l1_move():
    # The correct new state id
    new_state = np.array([
        [3,0,1,0],
        [0,2,1,0],
        [0,2,1,1],
        [0,2,2,3]])
    new_state_id = game.state_to_id(new_state)

    # The actual state id after the move
    new_move = np.array([[0,2],[1,2],[2,2],[2,3]])
    state_id, reward, termination, msgs = player1.move(new_move)

    assert state_id == new_state_id
    assert reward == -1
    assert termination == False
    assert msgs == "L-piece moved"

def test_l2_and_n_move():
    # The correct new state id
    new_state = np.array([
        [3,0,1,0],
        [0,3,1,0],
        [2,0,1,1],
        [2,2,2,0]])
    new_state_id = game.state_to_id(new_state)

    # The actual state id after the move
    new_move = np.array([[2,0],[3,0],[3,1],[3,2]])
    n_pos = np.array([[3,3],[1,1]])
    state_id, reward, termination, msgs = player2.move(new_move,n_pos)

    assert state_id == new_state_id
    assert reward == -1
    assert termination == False
    assert msgs == "L-piece moved, N-piece moved"

def test_l1_move_and_illegal_n_move():
    # The correct new state id
    new_state = np.array([
        [3,0,1,1],
        [0,3,1,0],
        [2,0,1,0],
        [2,2,2,0]])
    new_state_id = game.state_to_id(new_state)

    # The actual state id after the move
    new_move = np.array([[0,3],[0,2],[1,2],[2,2]])
    n_pos = np.array([[0,0],[3,0]])
    state_id, reward, termination, msgs = player1.move(new_move,n_pos)

    assert state_id == new_state_id
    assert reward == -1
    assert termination == False
    assert msgs == "L-piece moved, illegal N-move"

def test_win():
    win_state = np.array([
        [0,0,3,0],
        [1,1,1,0],
        [2,0,1,0],
        [2,2,2,3]])
    win_state_id = game.state_to_id(win_state)

    move1_l2 = np.array([[3,1],[3,2],[3,3],[2,3]])
    move1_n = np.array([[1,1],[1,3]])

    move2_l1 = np.array([[0,2],[0,1],[1,1],[2,1]])

    move3_l2 = np.array([[2,0],[3,0],[3,1],[3,2]])
    move3_n = np.array([[0,0],[3,3]])

    move4_l1 = np.array([[1,0],[1,1],[1,2],[2,2]])
    move4_n = np.array([[1,3],[0,2]])

    state_id, reward, termination, msgs = player2.move(move1_l2,move1_n)
    state_id, reward, termination, msgs = player1.move(move2_l1)
    state_id, reward, termination, msgs = player2.move(move3_l2,move3_n)
    state_id, reward, termination, msgs = player1.move(move4_l1,move4_n)

    assert state_id == win_state_id
    assert reward == 100
    assert termination == True
    assert msgs == "Won"

def test_reset():
    reset_state = np.array([
        [3,1,1,0],
        [0,2,1,0],
        [0,2,1,0],
        [0,2,2,3]])
    reset_state_id = game.state_to_id(reset_state)

    state_id, reward, termination, msgs = game.reset()

    assert state_id == reset_state_id
    assert reward == 0
    assert termination == False
    assert msgs == "Reset"

def test_loss():
    loss_state = np.array([
        [0,2,0,0],
        [3,2,0,0],
        [1,2,2,3],
        [1,1,1,0]])
    loss_state_id = game.state_to_id(loss_state)

    move1_l1 = np.array([[0,2],[0,3],[1,3],[2,3]])
    move2_l2 = np.array([[0,1],[1,1],[2,1],[2,2]])
    move2_n = np.array([[0,0],[1,0]])
    move3_l1 = np.array([[2,0],[3,0],[3,1],[3,2]])
    move3_n = np.array([[3,3],[2,3]])

    state_id, reward, termination, msgs = player1.move(move1_l1)
    state_id, reward, termination, msgs = player2.move(move2_l2,move2_n)
    state_id, reward, termination, msgs = player1.move(move3_l1,move3_n)

    assert state_id == loss_state_id
    assert reward == -100
    assert termination == True
    assert msgs == "Lost"

#TODO: what about rewards when we lose/win on l2's turn? Manual fix?
