from GamePiece import GamePiece

class Lpiece(GamePiece):
    # Counting the number of L-pieces
    class_counter = 0

    def __init__(self,game,symbol,position):
        """
        Params:
            game (Lgame.Lgame): The game-object which the piece belongs to
            symbol (int): Symbol (0-9) for numeric representation
            position (numpy.ndarray): Squares occupied on the game board
        """

        # Setting the id of the piece
        id = Lpiece.class_counter
        Lpiece.class_counter += 1

        super().__init__(id,game,symbol,position)

        # Moving piece to initial position
        self.move(position,None,False)

    def move(self,new_pos,n_pos=None,remove_old_pos=True):
        """
        Params:
            new_pos (numpy.ndarray): The new squares the piece should occupy
            n_pos (numpy.ndarray, optional): Old and new position for the neutral piece
            remove_old_pos (bool): If the old position should be overwritten with 0's or not

        Returns:
            state_id (str): The id of the state the board is in after moving
            reward (int): The reward for the movement
            termination (bool): If the goal is reached or not
            msgs (str): Information about the action taken
        """

        # Default values
        reward = -1
        #termination = False
        msgs = "Illegal move"

        # Updating the game board
        old_pos = self.get_pos()
        symbol = self.to_symbol()
        board_updated = self.get_game().move_l(old_pos,new_pos,symbol,remove_old_pos)

        if board_updated:
            # Updating the piece position
            self.set_pos(new_pos)
            msgs = "L-piece moved"

            # Moving the N-piece
            # Making sure we recieved a proper N-pos
            if n_pos is not None and n_pos.shape == (2,2):
                old_n_pos,new_n_pos = n_pos

                # Finding the correct N-piece object
                n_piece = None
                for n in self.get_game().get_n_pieces():
                    actual_n_pos = n.get_pos()
                    if actual_n_pos[0] == old_n_pos[0] and actual_n_pos[1] == old_n_pos[1]:
                        n_piece = n

                if n_piece is not None:
                    #TODO h??ndter dette?

                    moved_n_piece = n_piece.move(new_n_pos,remove_old_pos)
                    if moved_n_piece:
                        msgs += ", N-piece moved"
                    else:
                        msgs += ", illegal N-move"
                else:
                    msgs += ", illegal N-move"

            if self.get_game().has_won(self.to_symbol()):
                reward = 100
                #termination = True
                msgs = "Won"
            elif self.get_game().has_lost(self.to_symbol()):
                reward = -100
                #termination = True
                msgs = "Lost"

        # The state id after the moving is done
        state_id = self.get_game().state_to_id()

        return state_id, reward, self.get_game().termination, msgs
