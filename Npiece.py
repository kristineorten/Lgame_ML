from GamePiece import GamePiece

class Npiece(GamePiece):
    class_counter = 0

    def __init__(self,game,sym,pos,unicode="\u272A"):
        id = Npiece.class_counter
        Npiece.class_counter += 1

        super().__init__(id,game,sym,pos,unicode)

    def move(self,new_pos):
        old_x,old_y = self.get_pos()
        new_x,new_y = new_pos

        self.game.state[old_x,old_y] = 0
        self.game.state[new_x,new_y] = self.to_symbol()

        self.set_pos(new_pos)
