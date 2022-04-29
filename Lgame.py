import numpy as np
from Lpiece import Lpiece
from Npiece import Npiece

class Lgame:
    def __init__(self):
        # Gameboard size
        self.x = 4
        self.y = 4

        # Numeric representation of the pieces
        nr_of_n_pieces = 2
        self.symbol_empty_sq = 0
        self.symbol_l = [1,2]
        self.symbol_n = [3]*nr_of_n_pieces

        # Game state
        self.state = np.zeros((self.x,self.y)).astype('int')

        self._set_n_all_pos() #fills up self.n_all_pos
        self._set_l_all_pos() #fills up self.l_all_pos

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

    def __str__(self):
        """
        Returns:
            (str): The state matrix in string format
        """
        return str(self.state)

    def get_state(self):
        """
        Returns:
            self.state (numpy.ndarray): The state matrix
        """
        return self.state

    def get_players(self):
        """
        Returns:
            self.l_pieces (numpy.ndarray): The player pieces
        """
        return self.l_pieces

    def get_n_pieces(self):
        """
        Returns:
            self.n_pieces (numpy.ndarray): The neutral pieces
        """
        return self.n_pieces

    def move_n(self,old_pos,new_pos,symbol,remove_old_pos=True):
        """
        Moving a neutral piece

        Params:
            old_pos (numpy.ndarray): The previous square the piece occupied
            new_pos (numpy.ndarray): The new square the piece should occupy
            symbol (int): The numeric symbol of the piece
            remove_old_pos (bool): If the old position should be overwritten with 0's or not

        Returns:
            (bool): Whether moving the piece was succsessful or not
        """

        old_x,old_y = old_pos
        new_x,new_y = new_pos

        # Making sure the position is legal
        if self._square_exists(new_x,new_y) and self._squares_are_free([new_pos]):

            # Emptying the old square
            if remove_old_pos:
                self.state[old_x,old_y] = 0

            # Filling the new square
            self.state[new_x,new_y] = symbol

            return True

        return False

    def move_l(self,old_pos,new_pos,symbol,remove_old_pos=True):
        """
        Moving a player piece

        Params:
            old_pos (numpy.ndarray): The previous squares the piece occupied
            new_pos (numpy.ndarray): The new squares the piece should occupy
            symbol (int): The numeric symbol of the piece
            remove_old_pos (bool): If the old position should be overwritten with 0's or not

        Returns:
            (bool): Whether moving the piece was succsessful or not
        """

        # Making sure the position is legal
        if self._is_l_shaped(new_pos) and self._squares_are_free(new_pos,symbol):

            # Emptying the old squares
            if remove_old_pos:
                for pos in old_pos:
                    old_x,old_y = pos
                    self.state[old_x,old_y] = 0

            # Filling the new squares
            for pos in new_pos:
                new_x,new_y = pos
                if not self._square_exists(new_x,new_y):
                    return False #TODO
                self.state[new_x,new_y] = symbol

            return True

        return False

    def reset(self):
        """
        Returning the game board to the original state

        Returns:
            state_id (str): The id of the state the board is in after moving
            reward (int): The reward for the movement
            termination (bool): If the goal is reached or not
            msgs (str): Information about the action taken
        """
        # Resetting state to 0's
        self.state = np.zeros((self.x,self.y))

        # Placing player pieces
        for i in range(len(self.l_pieces)):
            self.l_pieces[i].move(self.l_pos_init[i],None,False)

        # Placing neutral pieces
        for i in range(len(self.n_pieces)):
            self.n_pieces[i].move(self.n_pos_init[i],False)

        # The id of the state after moving
        state_id = self.state_to_id()

        return state_id, 0, False, "Reset"

    def has_lost(self,l_sym): #TODO
        l_positions = self._find_available_l_pos(l_sym)
        if len(l_positions) > 1: # Has possible moves
            return False
        return True

    def has_won(self,l_sym): #TODO
        l2_sym = self.symbol_l[0]
        if l_sym == l2_sym:
            l2_sym = self.symbol_l[1]

        l2_positions = self._find_available_l_pos(l2_sym)
        if len(l2_positions) > 1: # L2 has possible moves
            return False

        return True

    def state_to_id(self,state=None):
        """
        Converting from state to state id

        Params:
            state (numpy.ndarray): The state we want to convert

        Returns:
            state_id (str): The state id
        """
        # Using the current state if no state is supplied
        if state is None:
            state = self.state

        # Converting to id-string
        state_id = ""
        for x in range(self.x):
            for y in range(self.y):
                state_id += str(int(state[x][y]))

        return state_id

    def to_unicode(self,state=None):
        """
        Converting from numeric state matrix to unicode state matrix

        Params:
            state (numpy.ndarray): The state we want to convert

        Returns:
            unicode_state (numpy.ndarray): The unicode state matrix
        """
        # Using the current state if no state is supplied
        if state is None:
            state = self.state

        # Unicode symbols for the neutral pieces
        n_unicode = np.array([""]*len(self.n_pieces))
        for i in range(len(n_unicode)):
            n_unicode[i] = self.n_pieces[i].to_unicode()#"\u272A"

        # Unicode symbols for the l-pieces (the L-shaped player pieces)
        l_unicode = np.array([""]*len(self.l_pieces))
        for i in range(len(l_unicode)):
            l_unicode[i] = self.l_pieces[i].to_unicode()#"\u25A1", "\u25A0"

        # Unicode symbol for an empty square
        empty_sq = "\u00B7"

        # Converting the state
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
        """
        Printing the unicode representation of the state

        Params:
            state (numpy.ndarray): The state we want to print
        """
        # Converting state to unicode
        unicode_state = self.to_unicode(state)

        # Unicode symbol for space (to get a less compact printing)
        space = "\u0020"

        # Converting the unicode state to a string
        state_str = ""
        for x in range(self.x):
            for y in range(self.y):
                state_str += unicode_state[x][y]+space
            state_str += "\n"

        # Printing the state
        print(state_str)





    # Local methods

    def _square_exists(self,x,y):
        """
        Checking if the square supplied is within the boundaries of the game board

        Params:
            x (int): The x-value (row)
            y (int): The y-value (column)

        Returns:
            (bool): Whether the square is inside the game board or not
        """

        if (x >= 0 and x < self.x) and (y >= 0 and y < self.y):
            return True
        return False

    def _squares_are_free(self,squares,l_piece_symbol=0):
        """
        Checking if the squares supplied are possible to move to

        Params:
            squares (numpy.ndarray): The squares we want to check
            l_piece_symbol (int): The symbol of the piece we want to move (if l-piece)

        Returns:
            (bool): Whether we can move to the squares or not
        """

        for sq in squares:
            sq_symbol = self.state[sq[0],sq[1]]

            # The square is occupied
            if (sq_symbol != l_piece_symbol and sq_symbol != self.symbol_empty_sq):
                return False

        # All squares are free
        return True

    def _is_l_shaped(self,squares):
        """
        Check if the squares form an L-shape

        Params:
            squares (numpy.ndarray): Four squares

        Returns:
            is_l_shape (bool): If the squares form an l-shape or not
        """
        # Default values
        is_l_shape = False
        three_squares_line = False
        has_corner = False

        # Converting from np.ndarray to list and sorting
        squares = squares.tolist()
        squares.sort()

        # Lists for neighboring squares with respect to rows and columns
        x_neighbors = []
        y_neighbors = []

        # Finding neighboring squares
        for sq1 in squares:
            for sq2 in squares:
                if not np.array_equal(sq1,sq2):

                    # Same y-value
                    if sq1[0]+1 == sq2[0] and sq1[1] == sq2[1]:
                        if sq1 not in y_neighbors:
                            y_neighbors.append(sq1)
                        if sq2 not in y_neighbors:
                            y_neighbors.append(sq2)

                    # Same x-value
                    if sq1[1]+1 == sq2[1] and sq1[0] == sq2[0]:
                        if sq1 not in x_neighbors:
                            x_neighbors.append(sq1)
                        if sq2 not in x_neighbors:
                            x_neighbors.append(sq2)

        # The L-shape consists of a three square line with a corner on one end
        if len(x_neighbors) == 2 and len(y_neighbors) == 3:
            # There is a line in the y-direction
            three_squares_line = True

            # There is a corner on the end of the line
            for sq in x_neighbors:
                if y_neighbors[0] == sq or y_neighbors[2] == sq:
                    has_corner = True

        if len(y_neighbors) == 2 and len(x_neighbors) == 3:
            # There is a line in the x-direction
            three_squares_line = True

            # There is a corner on the end of the line
            for sq in y_neighbors:
                if x_neighbors[0] == sq or x_neighbors[2] == sq:
                    has_corner = True

        # The squares are L-shaped
        if three_squares_line and has_corner:
            is_l_shape = True

        return is_l_shape

    def _find_available_l_pos(self,l_sym): #TODO
        l_positions = []
        for pos in self.l_all_pos:
            if self._squares_are_free(pos,l_sym):
                l_positions.append(pos)
        return l_positions

    def _find_available_n_pos(self): #TODO
        n_positions = []
        for pos in self.n_all_pos:
            if self._squares_are_free([pos]):
                n_positions.append(pos)
        return n_positions

    def _set_n_all_pos(self):
        """
        Find all possible positions for a neutral piece
        """
        self.n_all_pos = []
        for i in range(self.x):
            for j in range(self.y):
                self.n_all_pos.append([i,j])

    def _set_l_all_pos(self):
        """
        Find all possible positions for a player piece
        """
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
