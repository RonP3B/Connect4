"""
*Referenciado y modificado de: 
    https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
"""

import numpy as np  
import pygame  
import sys
import math

class ConnectFour():
    def __init__(self, rows: int, columns: int):
        self.ROWS = rows
        self.COLUMNS = columns
        self.board = np.zeros((rows, columns), dtype = int)
    
    def is_valid_location(self, col: int) -> bool:
        return self.board[0][col] == 0
    
    def get_next_open_row(self,col:int) -> bool:
        for r in range(self.ROWS -1, -1, -1):
            if self.board[r][col] == 0: return r
    
    def drop_piece(self, row: int, col: int, piece: int) -> None:
        self.board[row][col] = piece
            
    def check_all_horizontals(self, four_connected: list) -> bool:
        for r in range(self.ROWS): 
            for c in range(self.COLUMNS - 3):
                if (self.board[r][c:c + 4] == four_connected).all(): 
                    return True
        return False
    
    def check_all_verticals(self, four_connected:list) -> bool:
        for c in range(self.COLUMNS):
            for r in range(self.ROWS - 3):
                if (self.board[r:r+4,c] == four_connected).all():
                    return True
        return False
    
    def check_all_diagonals(self, four_connected:list) -> bool:     
        for c in range(self.COLUMNS - 3):
            for r in range(self.ROWS - 3): 
                if ([self.board[r+x][c+x] for x in range(4)] == four_connected):
                    return True
        return False
    
    def check_all_negative_diagonals(self, four_connected:list) -> bool:
        for c in range(self.COLUMNS - 3):
            for r in range(3, self.ROWS):
                if [self.board[r-x][c+x] for x in range(4)] == four_connected:
                    return True
        return False
    
    def test_goal(self, piece: int) -> bool:
        four_connected = [piece for i in range(4)]
        
        if self.check_all_horizontals(four_connected): return True
        if self.check_all_verticals(four_connected): return True
        if self.check_all_diagonals(four_connected): return True
        if self.check_all_negative_diagonals(four_connected): return True
        
        return False
    
BLUE = (51, 51, 153)
WHITE = (237, 246, 249)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (230, 230, 0)

board = ConnectFour(6, 7)

SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 7) 

width = board.COLUMNS * SQUARESIZE
height = (board.ROWS + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)

game_over = False
turn = 0
curr_piece_color = RED

pygame.init()
myfont = pygame.font.SysFont("monospace", 75)

def draw_board(board: ConnectFour) -> None:
    for c in range(board.COLUMNS):  
        for r in range(board.ROWS):
            board_rec = (c * SQUARESIZE, (r * SQUARESIZE) + SQUARESIZE, SQUARESIZE, SQUARESIZE)
            center = (int((c * SQUARESIZE) + (SQUARESIZE / 2)), int((r * SQUARESIZE) + (SQUARESIZE / 2) + SQUARESIZE))
        
            pygame.draw.rect(screen, BLUE, board_rec)
            
            if board.board[r][c] == 0: pygame.draw.circle(screen, WHITE, center, RADIUS)
            elif board.board[r][c] == 1: pygame.draw.circle(screen, RED, center, RADIUS)
            else: pygame.draw.circle(screen, YELLOW, center, RADIUS)
    
    pygame.display.update()    
    
def draw_curr_piece(pos_x, color):
    center = (pos_x, int(SQUARESIZE / 2))
    pygame.draw.circle(screen, color, center, RADIUS)
     
def winning_game(player: int) -> None:
    global game_over
    
    pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
    
    color = (DARK_YELLOW, RED)[player == 1]
    label = myfont.render(f"Player {player} wins!", 1, color)
    screen.blit(label, (25, 10))     
                
    game_over = True
       
def play_ply(board, col, piece):
    global game_over, turn
    
    if board.is_valid_location(col):
        row = board.get_next_open_row(col)                    
        board.drop_piece(row, col, piece) 
                    
        if board.test_goal(piece): winning_game(piece)                    
        
        turn = (0, 1)[turn == 0]

def main():
    global curr_piece_color
    
    draw_board(board)
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                draw_curr_piece(posx, curr_piece_color)
                   
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posX = event.pos[0]
                col = int(math.floor(posX / SQUARESIZE))

                if turn == 0: play_ply(board, col, 1)
                else: play_ply(board, col, 2)
                    
                curr_piece_color = (RED, YELLOW)[turn != 0]
                
                if not game_over: draw_curr_piece(posx, curr_piece_color)
                
                draw_board(board)

                if game_over: pygame.time.wait(4000)
                                                     
if __name__ == '__main__':
    main()