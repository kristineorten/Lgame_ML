from GamePiece import GamePiece

class Lpiece(GamePiece):
    class_counter = 0

    def __init__(self,game,sym,pos,unicode):
        id = Lpiece.class_counter
        Lpiece.class_counter += 1

        super().__init__(id,game,sym,pos,unicode)

    def _squares_are_free(self, squares):
        for sq in squares:
            symbol = self.game.state[sq[0],sq[1]]
            if (symbol != self.to_symbol() and symbol != 0):
                return False
        return True

    def move(self,new_pos,n_pos=None):
        reward = -1
        termination = False
        msgs = "Illegal move"

        if self.game._is_l_shaped(new_pos) and self._squares_are_free(new_pos):
            msgs = "Moved"

            for pos in self.get_pos():
                x,y = pos
                self.game.state[x,y] = 0
            for pos in new_pos:
                x,y = pos
                self.game.state[x,y] = self.to_symbol()

            if n_pos is not None and n_pos.shape == (2,2):
                old_x,old_y = n_pos[0]
                symbol = self.game.state[old_x,old_y]

                if (symbol == 3 or symbol == 4):
                    new_x,new_y = n_pos[1]

                    symbol = self.game.state[old_x,old_y]

                    self.game.state[old_x,old_y] = 0
                    self.game.state[new_x,new_y] = symbol

            for pos in new_pos:
                x,y = pos
                self.game.state[x,y] = self.to_symbol()

            # TODO
            if False: #won:
                reward = 100
                termination = True
                msgs = "Won"
            elif False: #lost:
                reward = -100
                msgs = "Lost"

        return self.game.state_to_id(self.game.state), reward, termination, msgs
