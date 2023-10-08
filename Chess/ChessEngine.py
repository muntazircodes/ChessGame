class GameState():
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

    def makeMove(self, move):
            self.board[move.startRow][move.startCol] = "__"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)

            self.whiteToMove = not self.whiteToMove

    # THE FUNCTION TO UNDO THE MOVE
    def undoMove(self):
        if len(self.moveLog)!= 0:   # THE MOVE LIST MUST NOT BE EMPTY
            move = self.moveLog.pop() # THE POP FUNCTION WILL AUTOMATICLY POP THE LAST ELEMENT OF LIST THE LIST SO THE MOVE IS UNDO

            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            self.whiteToMove = not self.whiteToMove



class Move():

    # MAPS OF KEY AND VALUES TO CREATE NOTATION

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}  # THIS WILL HELP US TO LABEL THE ROWS ON THE BASIS OF THEIR INDEXES

    rowsToRanks = {v:k for k, v in ranksToRows.items()}

    filesToCols = {"a" :0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}   # THIS WILL HELP US TO LABEL THE COLS ON THE BASIS OF THEIR INDEXES
    
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow  = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):

        # WE ADD THIS LINE TO GET THE REAL CHESS NOTATION
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]