from GamePiece import GamePiece

class Npiece(GamePiece):
    # Counting the number of N-pieces
    class_counter = 0

    def __init__(self,game,symbol,position,unicode="\u272A"):
        """
        Params:
            game (Lgame.Lgame): The game-object which the piece belongs to
            symbol (int): Symbol (0-9) for numeric representation
            position (numpy.ndarray): Squares occupied on the game board
            unicode (string): Symbol for unicode representation
        """

        # Setting the id of the piece
        id = Npiece.class_counter
        Npiece.class_counter += 1

        super().__init__(id,game,symbol,position,unicode)

    def move(self,new_pos,remove_old_pos=True):
        """
        Params:
            new_pos (numpy.ndarray): The new squares the piece should occupy
            remove_old_pos (bool): If the old position should be overwritten with 0's or not
        """

        # Updating the game board
        old_pos = self.get_pos()
        symbol = self.to_symbol()
        board_updated = self.get_game().move_n(old_pos,new_pos,symbol,remove_old_pos)

        # Updating the piece position
        if board_updated:
            self.set_pos(new_pos)
            return True

        return False
