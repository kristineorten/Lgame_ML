import numpy as np
from Lpiece import Lpiece
from Npiece import Npiece

class Lgame:
    def __init__(self):
        # Gameboard size:
        self.x = 4 #possible to make one with another size?
        self.y = 4

        # Numeric representation:
        nr_of_n_pieces = 2
        self.symbol_empty_sq = 0
        self.symbol_l = [1,2]
        self.symbol_n = [3]*nr_of_n_pieces

        # Game state
        self.state = np.zeros((self.x,self.y)) # The state is the game board

        # Neutral pieces (N)
        self.n_pieces = np.array([None]*nr_of_n_pieces)
        self.n_pos_init = np.array([[0,0],[3,3]])
        for i in range(len(self.n_pieces)):
            self.n_pieces[i] = Npiece(self,self.symbol_n[i],self.n_pos_init[i])

        # Player pieces (L)
        nr_of_l_pieces = 2
        l_pos_nr_of_sq = 4
        self.l_pieces = np.array([None,None])
        self.l_pos_init = np.zeros([nr_of_n_pieces,l_pos_nr_of_sq,2]).astype('int')
        self.l_pos_init[0] = np.array([[0,1],[0,2],[1,2],[2,2]])
        self.l_pos_init[1] = np.array([[1,1],[2,1],[3,1],[3,2]])
        self.l_pieces[0] = Lpiece(self,1,self.l_pos_init[0],"\u25A1")
        self.l_pieces[1] = Lpiece(self,2,self.l_pos_init[1],"\u25A0")

        self._find_all_n_pos() #fills up self.n_all_pos
        self._find_all_l_pos() #fills up self.l_all_pos

        self.reset()

    def get_players(self):
        return self.l_pieces

    def move_n(self,old_pos,new_pos,symbol):
        old_x,old_y = old_pos
        new_x,new_y = new_pos

        self.state[old_x,old_y] = 0
        self.state[new_x,new_y] = symbol

    def reset(self):
        # Resetting state to 0's
        self.state = np.zeros((self.x,self.y))

        # Placing player pieces
        for i in range(len(self.l_pieces)):
            self.l_pieces[i].move(self.l_pos_init[i])

        # Placing neutral pieces
        for i in range(len(self.n_pieces)):
            self.n_pieces[i].move(self.n_pos_init[i])

        return self.state_to_id(self.state), 0, False, "Reset"

    def __str__(self):
        return self.state

    def get_state(self):
        return self.state

    def state_to_id(self,state=None):
        if state is None:
            state = self.state

        state_str = ""
        for x in range(self.x):
            for y in range(self.y):
                state_str += str(int(state[x][y]))

        return state_str

    def to_unicode(self,state=None):
        if state is None:
            state = self.state

        n_unicode = np.array([""]*len(self.n_pieces))
        for i in range(len(n_unicode)):
            n_unicode[i] = self.n_pieces[i].to_unicode()#"\u272A"

        l_unicode = np.array([""]*len(self.l_pieces))
        for i in range(len(l_unicode)):
            l_unicode[i] = self.l_pieces[i].to_unicode()#"\u25A1", "\u25A0"

        empty_sq = "\u00B7"

        unicode_state = np.zeros((self.x,self.y)).astype('str')
        for x in range(self.x):
            for y in range(self.y):
                symbol = state[x][y]
                if symbol == self.symbol_l[0]:
                    unicode_state[x][y] = l_unicode[0]
                elif symbol == self.symbol_l[1]:
                    unicode_state[x][y] = l_unicode[1]
                elif symbol == self.symbol_n[0]:
                    unicode_state[x][y] = n_unicode[0]
                elif symbol == self.symbol_n[1]:
                    unicode_state[x][y] = n_unicode[1]
                else:
                    unicode_state[x][y] = empty_sq

        return unicode_state

    def print_unicode(self,state=None):
        unicode_state = self.to_unicode(state)
        space = "\u0020"

        state_str = ""
        for x in range(self.x):
            for y in range(self.y):
                state_str += unicode_state[x][y]+space
            state_str += "\n"

        print(state_str)

    """def add_Lpieces(self,L1,L2):
        self.l_pieces[0] = L1
        self.l_pieces[1] = L2
        self.reset()"""

    def _is_l_shaped(self,squares):
        """
        Check if the squares form an L-shape

        Params:
            squares: Four squares

        Returns:
            is_l_shape: If the squares form an l-shape or not
        """
        is_l_shape = False
        squares = squares.tolist()
        squares.sort()
        three_squares_line = False
        has_corner = False

        x_neighbors = []
        y_neighbors = []

        # L-shape if the three spares with the same x/y values has an inc or dec y/x value
        for sq1 in squares:
            for sq2 in squares:
                if not np.array_equal(sq1,sq2):

                    if sq1[0]+1 == sq2[0] and sq1[1] == sq2[1]:
                        if sq1 not in y_neighbors:
                            y_neighbors.append(sq1)
                        if sq2 not in y_neighbors:
                            y_neighbors.append(sq2)

                    if sq1[1]+1 == sq2[1] and sq1[0] == sq2[0]:
                        if sq1 not in x_neighbors:
                            x_neighbors.append(sq1)
                        if sq2 not in x_neighbors:
                            x_neighbors.append(sq2)

        # L-shape if one of the end squares have a neighboring square on another row/col
        if len(x_neighbors) == 2 and len(y_neighbors) == 3:
            three_squares_line = True

            for sq in x_neighbors:
                if y_neighbors[0] == sq or y_neighbors[2] == sq:
                    has_corner = True

        if len(y_neighbors) == 2 and len(x_neighbors) == 3:
            three_squares_line = True

            for sq in y_neighbors:
                if x_neighbors[0] == sq or x_neighbors[2] == sq:
                    has_corner = True

        if three_squares_line and has_corner:
            is_l_shape = True

        return is_l_shape

    def _find_all_n_pos(self):
        self.n_all_pos = []
        for i in range(self.x):
            for j in range(self.y):
                self.n_all_pos.append([i,j])

    def _find_all_l_pos(self):
        self.l_all_pos = []

        for sq1 in self.n_all_pos:
            for sq2 in self.n_all_pos:
                for sq3 in self.n_all_pos:
                    for sq4 in self.n_all_pos:

                        if sq1 not in [sq2,sq3,sq4] and sq2 not in [sq3,sq4] and sq3 not in [sq4]:
                            new_pos = [sq1,sq2,sq3,sq4]
                            new_pos.sort()

                            if self._is_l_shaped(np.array(new_pos)) and new_pos not in self.l_all_pos:
                                self.l_all_pos.append(new_pos)

    def write_to_file_all_states(self,filename):
        """
        Writing all possible states to file
        Previous format: l1_pos:l2_pos:n1_pos:n2_pos
        Current format: state_id

        Params:
            filename: the name of the file
        """

        all_states = []
        file = open(filename,"w")
        for l1_pos in self.l_all_pos:
            for l2_pos in self.l_all_pos:

                legal_l_pos = True
                for pos in l1_pos:
                    if pos in l2_pos:
                        legal_l_pos = False
                if legal_l_pos:

                    for n1_pos in self.n_all_pos:
                        if (n1_pos not in l1_pos) and (n1_pos not in l2_pos):

                            for n2_pos in self.n_all_pos:
                                if (n1_pos != n2_pos) and (n2_pos not in l1_pos) and (n2_pos not in l2_pos):

                                    # Making the state
                                    state = np.zeros((self.x,self.y))
                                    positions = [l1_pos,l2_pos,[n1_pos],[n2_pos]]
                                    for i in range(len(positions)):
                                        for pos in positions[i]:
                                            pos_x,pos_y = pos
                                            state[pos_x,pos_y] = min(i+1,len(positions)-1)
                                    state_id = self.state_to_id(state)

                                    # Adding to list and file
                                    if (state_id not in all_states):
                                        state90 = np.rot90(state)
                                        state180 = np.rot90(state90)
                                        state270 = np.rot90(state180)

                                        state90_id = self.state_to_id(state90)
                                        state180_id = self.state_to_id(state180)
                                        state270_id = self.state_to_id(state270)

                                        # Adding all to all_states
                                        all_states.extend([state_id,state90_id,state180_id,state270_id])
                                        # Adding only one to the file
                                        file.write(state_id+"\n")
        file.close()
