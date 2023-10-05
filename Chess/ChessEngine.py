class GameState:
    def __init__(self):


        # THIS IS THE 8 * 8 2D LIST WHICH HAS 2 CHARACTERS. 
        # THE FIRST CHARACTER REPRENSTS THE COLOR AND THE SECOND CHARACTER REPRESENTS THE PIECE.

        self.board = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["__", "__", "__", "__", "__", "__", "__", "__"],
                ["__", "__", "__", "__", "__", "__", "__", "__"],
                ["__", "__", "__", "__", "__", "__", "__", "__"],
                ["__", "__", "__", "__", "__", "__", "__", "__"],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        
        # THIS WILL HELP TO TOGGLE AND CHANGING THE TURNS AFTER WE WILL CREATE A FUNCTION LATER ON
        self.whiteToMove = True
        # THIS WILL KEEP THE TRACK OF MOVES
        self.moveLog = []