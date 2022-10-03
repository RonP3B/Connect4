import numpy as np 
import pygame 
from Classes import Class_ConnectFour as CF
from Helpers import GameManagement as GM

BLUE = (51, 51, 153)
WHITE = (237, 246, 249)
RED = (255, 0, 0)
YELLOW = (255, 235, 10)
DARK_YELLOW = (230, 230, 0)
SQUARESIZE = 100
board = CF.ConnectFour(np.zeros((6, 7), dtype=int), 6, 7)
width = board.COLUMNS * SQUARESIZE
height = (board.ROWS + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
RADIUS = int(SQUARESIZE / 2 - 7) 

pygame.init()

myfont = pygame.font.SysFont("monospace", 75)

def draw_board(board: CF.ConnectFour) -> None:
    for c in range(board.COLUMNS):  
        for r in range(board.ROWS):
            board_rec = (c * SQUARESIZE, (r * SQUARESIZE) + SQUARESIZE, SQUARESIZE, SQUARESIZE)
            center = (int((c * SQUARESIZE) + (SQUARESIZE / 2)), int((r * SQUARESIZE) + (SQUARESIZE / 2) + SQUARESIZE))
            
            pygame.draw.rect(screen, BLUE, board_rec)
            
            if board.board[r][c] == 0: pygame.draw.circle(screen, WHITE, center, RADIUS)
            elif board.board[r][c] == 1: pygame.draw.circle(screen, RED, center, RADIUS)
            else: pygame.draw.circle(screen, YELLOW, center, RADIUS)
                     
    pygame.display.update()    
    
def draw_piece(center: float) -> None:    
    pygame.draw.circle(screen, RED, center, RADIUS)
    
def draw_top() -> None:
    pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))

def remove_piece_from_top() -> None:
    draw_top()      
    pygame.display.update()
     
def winning_game(player: int) -> None:
    remove_piece_from_top()
    color = (DARK_YELLOW, RED)[player == GM.HUMAN_PLAYER]
    msg = ("The AI beat you", "You have won!!!")[player == GM.HUMAN_PLAYER]
    label = myfont.render(msg, 1, color)
    screen.blit(label, (20, 10))                  
    GM.end_game()
    
def tied_game() -> None:
    remove_piece_from_top()
    label = myfont.render(f"Game tied", 1, BLUE)
    screen.blit(label, (150, 10))                           
    GM.end_game()
    