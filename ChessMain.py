# IMPORTING PYGAME FOR THE GAME INTERFACE
import pygame as p
# IMPORTING "ChessEngine" AS MODULE TO USE IN THIS PROJECT
from Chess import ChessEngine


# DIMENSIONS OF THE CHESS BOARD

WIDTH = HEIGHT = 512            # THIS WILL GIVE THE HEIGHT AND WIDTH OF THE BOARD
DIMENSION = 8                   # THE DIMENSION WILL HELP IN GET THE SECTION
SQ_SIZE = WIDTH // 8            # THIS WILL GIVE THE EQUAL SQUARE SIZE

MAX_FPS = 25                    # THE FRAME RATES 

IMAGES = {}                     # THIS DICTIONARY WILL HELP TO HANDLE THE IMAGES

# THE FUNCTION WILL HELP TO LOAD THE IMAGES
def loadImages():

    # DETERMINE THE EXACT NAME OF EACH PIECE THATS WHY WE NAMED THE PIECES IN THE BOARD EXACT AS NAME OF THE IMAGES
    pieces = ["wp", "bp", "wR", "bR", "wN", "bN", "wB", "bB", "wQ", "bQ", "bK", "wK"]

    # ITERATING THE LIST TO GET EACH NAME ONE BY ONE
    for piece in pieces:
        # LOADING THE IMAGES AND RESIZING THE IMAGES EXACTLY IN THE SIZE ON SQ_SIZE SO IT WILL EXACTLY FIT THE BOARD 
        IMAGES[piece] = p.transform.scale(p.image.load("Images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))

# THE MAIN FUNCTION TO EXECUTE THE FILE
def main():
    
    p.init() # INITIALISING THE PYGAME

    screen = p.display.set_mode((WIDTH, HEIGHT)) # THE SCREEN THAT WILL BE DISPLAYED FOR GAME
    clock = p.time.Clock()  
    screen.fill(p.Color("white")) # COLOR OF THE BG SCREEN
    gs = ChessEngine.GameState() # CALLING THE MAIN GAMESTATE FUNCTION
    loadImages() # LOADING THE IMAGES

    running = True
    while running:
        # THIS FUNCTION WILL HELP TO QUIT THE GAME
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        # THIS WILL EXECUTE AND SCREEN AND PIECES WILL BE CREATED ON INITIALIZNG THE BOARD
        drawGamestate(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

# THIS FUNCTION ON EXECUTING RUN TWO FUNTION AND WILL DRAW THE WHOLE CHESS BOARD
def drawGamestate(screen , gs):

    # FUNCTION WILL DRAW BOARD
    drawBoard(screen)
    # THIS FUNCTION WILL DRAW PIECES
    drawPieces(screen , gs.board)

# THE BOARD DRAWING FUNCTION
def drawBoard(screen):
    # THE COLORS WILL BE PICKED WITH THE HELP OF LIST AND LOOPS
    colors = [p.Color("white"), p.Color("gray")]
    
    # BOTH LOOPS WILL INITIALIZE AND RUN FROM 0 TO 7
    for r in range(DIMENSION):
        for c in range(DIMENSION):

            # THIS ALGORITHIM WILL CHOOSE THE COLOR IF THE SUM OF ROW NO AND COL NO IS EVEN COLOR WILL BE WHITE ELSE GRAG
            color = colors[((r+c) % 2)]
            # DRAW THE SQUARE OF THE BOARD
            p.draw.rect(screen, color,p.Rect(c *SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# THE FUNCTION TO DRAW PIECES ON THE SCREEN
def drawPieces(screen , board):

    for r in range(DIMENSION):
        for c in range(DIMENSION):

            # THIS WILL GET US THE LAST CHARACTER OF THE IMAGE
            piece = board[r][c]
            if piece != "__":

                # SETTING THE IMAGES AT EXACTLY AT THE PLACE OF SQUARES SO THE CHESS BOARD WILL BE DRAWN
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# THE MAIN FUNCTION TO RUN THE FILE
if __name__ == "__main__":
    main()