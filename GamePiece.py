class GamePiece:
    def __init__(self,id,game,symbol,position,unicode):
        """
        Params:
            id (int): id (relative to subclass)
            game (Lgame): the game-object which the piece belongs to
            symbol (int): symbol (0-9) for numeric representation
            position (ndarray): squares occupied on the game board
            unicode (string): symbol for unicode representation
        """
        self.id = id
        self.symbol = symbol
        self.position = position
        self.unicode = unicode
        self.game = game

    def get_id(self):
        return self.id

    def __str__(self):
        return self.symbol

    def to_symbol(self):
        return self.symbol

    def to_unicode(self):
        return self.unicode

    def print_symbol(self):
        print(self.to_symbol())

    def print_unicode(self):
        print(self.to_unicode())

    def get_pos(self):
        return self.position

    def set_pos(self,new_pos):
        self.position = new_pos
