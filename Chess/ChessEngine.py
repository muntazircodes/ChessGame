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
        
        self.moveFunction = {'p':self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                             'B': self.getBishopMoves, 'Q':self.getQueenMoves, 'K': self.getKingMoves}
        
        # THIS WILL HELP TO TOGGLE AND CHANGING THE TURNS AFTER WE WILL CREATE A FUNCTION LATER ON
        self.whiteToMove = True
        # THIS WILL KEEP THE TRACK OF MOVES
        self.moveLog = []

        # KEEPING TRACK OF KING LOCATIONS
        self.whiteKingLocation = (7, 4) # WHITE KING'S INITIAL LOCATION AT ROW 7, COLUMN 4
        self.blackKingLocation = (0, 4) # BLACK KING'S INITIAL LOCATION AT ROW 0, COLUMN 4

        self.checkMate = False # CHECK IF THE KING IS IN CHECK AND THERE IS NO VALID MOVES TO PLAY
        self.staleMate = False # CHECK IF THE KING IS NOT IN CHECK AND THERE IS NO MOVES TO PLAY

    def makeMove(self, move):
        # UPDATE THE BOARD AFTER A MOVE
        self.board[move.startRow][move.startCol] = "__"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # ADD MOVE TO THE LOG

        self.whiteToMove = not self.whiteToMove # SWITCH TURN

        # UPDATE KING'S LOCATION AFTER MOVE
        if move.pieceMoved == "wK":
            self.whiteKingLocation =(move.endRow, move.endCol) # UPDATE WHITE KING'S LOCATION
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol) # UPDATE BLACK KING'S LOCATION

    # FUNCTION TO UNDO A MOVE
    def undoMove(self):
        if len(self.moveLog) != 0: # ENSURE THE MOVE LIST IS NOT EMPTY
            move = self.moveLog.pop() # GET THE LAST MOVE FROM THE LIST

            # REVERT THE BOARD TO THE PREVIOUS STATE
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            self.whiteToMove = not self.whiteToMove # SWITCH TURN

            # REVERT KING'S LOCATION AFTER UNDOING MOVE
            if move.pieceMoved == "wK":
                self.whiteKingLocation =(move.startRow, move.startCol) # REVERT WHITE KING'S LOCATION
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol) # REVERT BLACK KING'S LOCATION

    # FUNCTION TO GET VALID MOVES CONSIDERING CHECKS
    def getValidMoves(self):
        moves = self.getAllPossibleMoves() # GENERATE ALL POSSIBLE MOVES

        valid_moves = []

        for i in range(len(moves)-1, -1, -1): # ITERATE THROUGH THE MOVES
            self.makeMove(moves[i]) # MAKE THE MOVE

            # SWITCH TURN TO GET OPPONENT'S MOVES
            self.whiteToMove = not self.whiteToMove

            # CHECK IF THE MOVE PUTS THE KING IN CHECK
            if self.inCheck():
                moves.remove(moves[i]) # IF SO, IT'S NOT A VALID MOVE

            # SWITCH TURN BACK AND UNDO THE MOVE
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:

            if self.inCheck():
                
                self.checkMate = True
            else:
                self.staleMate = False
        else:
            self.checkMate = False
            self.staleMate = False

        return moves

    # FUNCTION TO CHECK IF THE CURRENT PLAYER IS IN CHECK
    def inCheck(self):
        if self.whiteToMove:
            return self.squaresUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squaresUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # FUNCTION TO CHECK IF A SQUARE IS UNDER ATTACK
    def squaresUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # SWITCH TURN

        oppMoves = self.getAllPossibleMoves() # GET OPPONENT'S MOVES

        self.whiteToMove = not self.whiteToMove # SWITCH TURN BACK

        for move in oppMoves: # CHECK IF ANY MOVE IS ATTACKING THE SQUARE
            if move.endRow == r and move.endCol == c:
                return True

        return False # SQUARE IS NOT UNDER ATTACK

    def getAllPossibleMoves(self): # ALL THE MOVES WITHOUT CONSIDERING CHECKS
        moves = [Move((6, 4), (4, 4), self.board)] # ADDED A MOVE FOR TESTING PURPOUSE
        for r in range(len(self.board)): # NUMBER OF ROWS 
            for c in range(len(self.board[r])): # NUMBER OF COLS IN A GIVEN ROW
                turn = self.board[r][c][0] # FOR GETTING THE COLOR OF PIECE THAT IS BIENG PLAYED
                
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove): # TOGGLE THE TURN BETWEEN THE PLAYES
                    piece = self.board[r][c][1] # GIVES THE NAME OF THE PIECE
                    self.moveFunction[piece](r, c, moves)

                  
        return moves

    # MOVES FOR PAWNS
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # WHEN WHITE PAWN MOVES

            if self.board[r - 1][c] == "__":  # 1 SQUARE PAWN ADVANCE
                moves.append(Move((r, c), (r-1, c) , self.board))

                if r == 6 and self.board[r - 2][c] == "__":  # 2 SQUARE PAWN ADVANCE
                    moves.append(Move((r, c), (r-2, c), self.board))

            if c - 1 >= 0: # CAPTURE TO THE LEFT
                if self.board[r -1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))

            if c + 1 <= 7: # CAPTURE TO THE RIGHT
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c]=="__":
                moves.append(Move((r, c), (r + 1, c), self.board))

                if r == 1 and self.board[r + 2][c] == "__":  
                    moves.append(Move((r, c), (r + 2, c), self.board))

            if c + 1 <= 7:  # CAPTURE TO THE RIGHT
                if self.board[r +1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

                    
            if c - 1 >= 0:  # CAPTURE TO THE LEFT
                if self.board[r + 1][c - 1][0] == "w":  
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))  


    # MOVES FOR ROOK

    # DEFINE A METHOD NAMED 'GETROOKMOVES' WHICH TAKES SELF (REFERRING TO THE INSTANCE OF THE CLASS), 
    # R (ROW POSITION OF THE ROOK), C (COLUMN POSITION OF THE ROOK), AND MOVES (LIST TO STORE POSSIBLE MOVES).
    def getRookMoves(self, r, c, moves):
        # DEFINE THE FOUR DIRECTIONS ROOK CAN MOVE: UP, LEFT, DOWN, AND RIGHT.
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1))
        
        # DETERMINE THE COLOR OF THE ENEMY PIECES BASED ON WHOSE TURN IT IS.
        enemyColor = "b" if self.whiteToMove else "w"
        
        # LOOP THROUGH EACH DIRECTION.
        for d in direction:
            # LOOP THROUGH A RANGE OF DISTANCES THE ROOK CAN MOVE, FROM 1 TO 7.
            for i in range(1, 8):
                # CALCULATE THE POTENTIAL ENDING ROW AND COLUMN FOR THE MOVE.
                endRow = r + d[0] * i 
                endCol = c + d[1] * i
                
                # CHECK IF THE POTENTIAL MOVE IS WITHIN THE BOUNDS OF THE BOARD.
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    # GET THE PIECE AT THE POTENTIAL ENDING POSITION.
                    endPiece = self.board[endRow][endCol]
                    
                    # IF THE ENDING POSITION IS EMPTY, ADD THE MOVE TO THE LIST OF POSSIBLE MOVES.
                    if endPiece == "__":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # IF THE ENDING POSITION CONTAINS AN ENEMY PIECE, ADD THE MOVE AND STOP LOOKING IN THIS DIRECTION.
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    # IF THE ENDING POSITION CONTAINS A FRIENDLY PIECE, STOP LOOKING IN THIS DIRECTION.
                    else:
                        break
                else:
                    # IF THE POTENTIAL MOVE IS OUT OF BOUNDS, STOP LOOKING IN THIS DIRECTION.
                    break


    # MOVES FOR KNIGHT
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2,  -1), (-2,  1), (-1, -2), (-1, 2), (1, -2), (1,  2), (2, -1), (2,  1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # MOVES FOR BISHOP
    def getBishopMoves(self, r, c, moves):
        # DEFINE THE FOUR DIAGONALS IN WHICH BISHOP CAN MOVE:
        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        
        # DETERMINE THE COLOR OF THE ENEMY PIECES BASED ON WHOSE TURN IT IS.
        enemyColor = "b" if self.whiteToMove else "w"
        
        # LOOP THROUGH EACH DIRECTION.
        for d in direction:
            # LOOP THROUGH A RANGE OF DISTANCES THE ROOK CAN MOVE, FROM 1 TO 7.
            for i in range(1, 8):
                # CALCULATE THE POTENTIAL ENDING ROW AND COLUMN FOR THE MOVE.
                endRow = r + d[0] * i 
                endCol = c + d[1] * i
                
                # CHECK IF THE POTENTIAL MOVE IS WITHIN THE BOUNDS OF THE BOARD.
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    # GET THE PIECE AT THE POTENTIAL ENDING POSITION.
                    endPiece = self.board[endRow][endCol]
                    
                    # IF THE ENDING POSITION IS EMPTY, ADD THE MOVE TO THE LIST OF POSSIBLE MOVES.
                    if endPiece == "__":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # IF THE ENDING POSITION CONTAINS AN ENEMY PIECE, ADD THE MOVE AND STOP LOOKING IN THIS DIRECTION.
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    # IF THE ENDING POSITION CONTAINS A FRIENDLY PIECE, STOP LOOKING IN THIS DIRECTION.
                    else:
                        break
                else:
                    # IF THE POTENTIAL MOVE IS OUT OF BOUNDS, STOP LOOKING IN THIS DIRECTION.
                    break

    # MOVES FOR QUEEN 
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    # MOVES FOR KING
    def getKingMoves(self, r, c, moves):
        knigMoves = ((-1,  -1), (-1,  0), (-1, 1), (0, -1), (0, 1), (1,  -1), (1, 0), (1,  1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + knigMoves[i][0]
            endCol = c + knigMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))



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

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    

    def getChessNotation(self):

        # WE ADD THIS LINE TO GET THE REAL CHESS NOTATION
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]