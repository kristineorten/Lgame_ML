import numpy as np
from Lpiece import Lpiece
from Npiece import Npiece
from Lgame import Lgame

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
