import pygame as p
from Chess import ChessEngine


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH // 8
MAX_FPS = 25
IMAGES = {}

def loadImages():
    pieces = ["wp", "bp", "wR", "bR", "wN", "bN", "wB", "bB", "wQ", "bQ", "bK", "wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()  
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        drawGamestate(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGamestate(screen , gs):

    drawBoard(screen)
    drawPieces(screen , gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color,p.Rect(c *SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen , board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "__":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()