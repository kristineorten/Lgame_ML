import constants as const

class GamePiece:
    def __init__(self,id,game,symbol,position):
        """
        Params:
            id (int): id (relative to subclass)
            game (Lgame.Lgame): The game-object which the piece belongs to
            symbol (int): Symbol (0-9) for numeric representation
            position (numpy.ndarray): Squares occupied on the game board
        """
        self.id = id
        self.symbol = symbol
        self.position = position
        self.unicode = const.to_unicode(symbol) #Symbol for unicode representation
        self.game = game

    def get_id(self):
        """
        Returns:
            self.id (int): The id of the piece
        """
        return self.id

    def __str__(self):
        """
        Returns:
            self.symbol (str): The piece symbol in string format
        """
        return str(self.symbol)

    def to_symbol(self):
        """
        Returns:
            self.symbol (int): The piece symbol
        """
        return self.symbol

    def to_unicode(self):
        """
        Returns:
            self.unicode (str): The piece unicode symbol
        """
        return self.unicode

    def print_symbol(self):
        """
        Prints the piece symbol
        """
        print(self.symbol)

    def print_unicode(self):
        """
        Prints the piece unicode symbol
        """
        print(self.unicode)

    def get_pos(self):
        """
        Returns:
            self.position (numpy.ndarray): The squares the piece occupies
        """
        return self.position

    def set_pos(self,new_pos):
        """
        Changing the position of the piece
        """
        self.position = new_pos

    def get_game(self):
        """
        Returns:
            game (Lgame.Lgame): The game-object which the piece belongs to
        """
        return self.game
