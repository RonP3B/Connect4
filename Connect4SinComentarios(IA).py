"""
*Diseño de la ventana del connect 4 referenciado y modificado de: 
    https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
"""

import numpy as np 
import pygame  
import sys
import math
import copy
import time

class ConnectFour():
    def __init__(self, board: list, rows: int, columns: int, parent = None):
        self.ROWS = rows
        self.COLUMNS = columns
        self.board = board
        
    def is_valid_location(self, col: int) -> bool:
        return self.board[0][col] == 0
    
    def get_next_open_row(self,col:int) -> int:
        for r in range(self.ROWS -1, -1, -1):
            if self.board[r][col] == 0: return r
    
    def drop_piece(self, row: int, col: int, piece: int) -> None:
        self.board[row][col] = piece
            
    def check_all_horizontals(self, four_connected: list) -> bool:
        for r in range(self.ROWS):
            for c in range(self.COLUMNS - 3):                
                if (self.board[r][c:c + 4] == four_connected).all(): return True
                
        return False
    
    def check_all_verticals(self, four_connected:list) -> bool:
        for c in range(self.COLUMNS):
            for r in range(self.ROWS - 3):
                if (self.board[r:r+4,c] == four_connected).all(): return True
                
        return False
    
    def check_all_diagonals(self, four_connected:list) -> bool:     
        for c in range(self.COLUMNS - 3):
            for r in range(self.ROWS - 3):         
                if ([self.board[r+x][c+x] for x in range(4)] == four_connected): return True
                
        return False
    
    def check_all_negative_diagonals(self, four_connected:list) -> bool:
        for c in range(self.COLUMNS - 3):
            for r in range(3, self.ROWS): 
                if [self.board[r-x][c+x] for x in range(4)] == four_connected: return True
        return False
    
    def expand(self, player: int) -> list:
        children = []
        
        for col in range(self.COLUMNS):
            if self.is_valid_location(col):
                nextOpenRow = self.get_next_open_row(col)
                newChild = ConnectFour(copy.copy(self.board), self.ROWS, self.COLUMNS, self) 
                newChild.drop_piece(nextOpenRow, col, player)
                children.append(newChild)
        
        return children
                
    
    def test_win(self, piece: int) -> bool:
        four_connected = [piece for i in range(4)]
        
        if self.check_all_horizontals(four_connected): return True
        if self.check_all_verticals(four_connected): return True
        if self.check_all_diagonals(four_connected): return True
        if self.check_all_negative_diagonals(four_connected): return True
        
        return False
    
    def test_tie(self) -> bool:
        for col in range(self.COLUMNS):
            if self.is_valid_location(col): return False
            
        return True

BLUE = (51, 51, 153)
WHITE = (237, 246, 249)
RED = (255, 0, 0)
YELLOW = (255, 235, 10)
DARK_YELLOW = (230, 230, 0)

board = ConnectFour(np.zeros((6, 7), dtype=int), 6, 7)

SQUARESIZE = 100

width = board.COLUMNS * SQUARESIZE

height = (board.ROWS + 1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)

RADIUS = int(SQUARESIZE / 2 - 7) 

game_over = False

HUMAN_PLAYER, AI_PLAYER = 1, 2

turn = AI_PLAYER

start_time = total_time = 0

failed_case = (None, None)

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

def remove_piece_from_top() -> None:
    pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))      
    pygame.display.update()
     
def winning_game(player: int) -> None:
    remove_piece_from_top()
    
    color = (DARK_YELLOW, RED)[player == HUMAN_PLAYER]
    
    msg = ("The AI beat you", "You have won!!!")[player == HUMAN_PLAYER]
    
    label = myfont.render(msg, 1, color)
    
    screen.blit(label, (20, 10)) 
                   
    end_game()
    
def tied_game() -> None:
    remove_piece_from_top()
    
    label = myfont.render(f"Game tied", 1, BLUE) 
                           
    screen.blit(label, (150, 10))   
                           
    end_game()
    
def end_game() -> None:
    global game_over
    
    game_over = True

def change_turn() -> None:
    global turn
    
    turn = (HUMAN_PLAYER, AI_PLAYER)[turn == HUMAN_PLAYER]
    
def is_time_over(start_time: float, total_time: float) -> bool:
    return time.time() - start_time >= total_time
    
def play_human_ply(board: ConnectFour, col: int) -> None:
    row = board.get_next_open_row(col)
    
    board.drop_piece(row, col, HUMAN_PLAYER)
    
    change_turn() 
  
def play_AI_ply(board: ConnectFour, total_seconds: int):
    global start_time, total_time
    
    total_time, start_time = total_seconds, time.time()
    
    depth, max_depth_allowed = 1, 100
    
    ply = None
    
    while depth < max_depth_allowed and not is_time_over(start_time, total_time):
        ply = decision(board, AI_PLAYER, depth, ply)
        depth += 1
       
    print(f"Profundidad alcanzada: {depth - 1}\n")
    
    board.board = ply.board
    
    change_turn()
    
def is_goal_state(board: ConnectFour, player: int) -> None:
    if board.test_win(player): winning_game(player)
    elif board.test_tie(): tied_game() 
        
max_depth = 0

def is_terminal(state: ConnectFour) -> bool:
    return state.test_win(AI_PLAYER) or state.test_win(HUMAN_PLAYER) or state.test_tie()
    
def min_value(state:ConnectFour, alpha, beta, piece:int, opp_piece:int, curr_depth = 0) -> tuple:       
    if is_time_over(start_time, total_time): return failed_case
    
    if is_terminal(state) or curr_depth == max_depth: return (None, eval(state, piece))
    
    minChild, minUtility = None, math.inf 
    
    for child in state.expand(opp_piece):
        _, utility = max_value(child, alpha, beta, piece, opp_piece, curr_depth + 1)
        
        if utility == None: return failed_case
           
        if utility < minUtility: minChild, minUtility = child, utility
        
        if minUtility <= alpha: break
            
        if minUtility < beta: beta = minUtility
                 
    return (minChild, minUtility)
        
def max_value(state:ConnectFour, alpha, beta, piece:int, opp_piece:int, curr_depth:int = 0) -> tuple:        
    if is_time_over(start_time, total_time): return failed_case
    
    if  is_terminal(state) or curr_depth == max_depth: return (None, eval(state, piece))

    maxChild, maxUtility = None, -math.inf 
      
    for child in state.expand(piece): 
        _, utility = min_value(child, alpha, beta, piece, opp_piece, curr_depth + 1) 
        
        if utility == None: return failed_case
           
        if utility > maxUtility: maxChild, maxUtility = child, utility 
        
        if maxUtility >= beta: break
        
        if maxUtility > alpha: alpha = maxUtility
                     
    return (maxChild, maxUtility)

def decision(state: ConnectFour, piece: int, depth: int, last_ply: ConnectFour) -> ConnectFour:     
    global max_depth 

    max_depth = depth
    
    opp_piece = (HUMAN_PLAYER, AI_PLAYER)[piece == 1]
    
    child, _ = max_value(state, -math.inf, math.inf, piece, opp_piece)   
    
    return (last_ply, child)[child != None]
    
def eval_space(piece: int, space: list) -> int:
    utility = 0
    
    opp_piece = (HUMAN_PLAYER, AI_PLAYER)[piece == HUMAN_PLAYER]

    if space.count(piece) == 4: utility += 50
    elif space.count(piece) == 3 and space.count(0) == 1: utility += 6
    elif space.count(piece) == 2 and space.count(0) == 2: utility += 1
               
    if space.count(opp_piece) == 4: utility -= 50
    elif space.count(opp_piece) == 3 and space.count(0) == 1: utility -= 10 
    elif space.count(opp_piece) == 2 and space.count(0) == 2: utility -= 1
    
    return utility

def eval(board: ConnectFour, piece: int) -> int:
    utility = 0
    
    centerColumn = [i for i in board.board[:,board.COLUMNS // 2]]
    
    utility += centerColumn.count(piece) * 3
    
    for r in range(board.ROWS): 
        for c in range(board.COLUMNS - 3):
            current_space = list(board.board[r][c:c + 4])
            utility += eval_space(piece, current_space)
           
    for c in range(board.COLUMNS):
        for r in range(board.ROWS - 3):
            current_space = list(board.board[r:r + 4, c])
            utility += eval_space(piece, current_space)
            
    for c in range(board.COLUMNS - 3):
        for r in range(board.ROWS - 3): 
            current_space = [board.board[r+x][c+x] for x in range(4)]
            utility += eval_space(piece, current_space)    
        
    for c in range(board.COLUMNS - 3):
        for r in range(3, board.ROWS):
            current_space = [board.board[r-x][c+x] for x in range(4)]
            utility += eval_space(piece, current_space)
            
    return utility

def main():
    global turn
        
    draw_board(board)
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
                
            if event.type == pygame.MOUSEMOTION and turn == HUMAN_PLAYER:
                posX = event.pos[0]
                center = (posX, int(SQUARESIZE / 2))
                
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                pygame.draw.circle(screen, RED, center, RADIUS)
                   
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == HUMAN_PLAYER:
                posX = event.pos[0]  
                col = int(math.floor(posX / SQUARESIZE))
                
                if board.is_valid_location(col):
                    play_human_ply(board, col)
                    is_goal_state(board, HUMAN_PLAYER)
                    draw_board(board)

        if turn == AI_PLAYER and not game_over:
            remove_piece_from_top()
            play_AI_ply(board, 2)
            is_goal_state(board, AI_PLAYER)
            draw_board(board)
             
        if game_over: pygame.time.wait(7000)
                                       
if __name__ == '__main__':
    main()