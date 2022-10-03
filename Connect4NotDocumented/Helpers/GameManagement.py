import time
from Classes import Class_ConnectFour as CF
from Helpers import BoardManagement as BM
from Minimax import Desicion as DS

game_over = False
HUMAN_PLAYER, AI_PLAYER = 1, 2
start_time = total_time = 0
failed_case = (None, None)
max_depth = 0 
turn = 2 

def end_game() -> None:
    global game_over
    game_over = True

def change_turn() -> None:
    global turn
    turn = (HUMAN_PLAYER, AI_PLAYER)[turn == HUMAN_PLAYER]

def is_time_over(start_time: float, total_time: float) -> bool:
    return time.time() - start_time >= total_time
  
def play_human_ply(board: CF.ConnectFour, col: int) -> None:
    row = board.get_next_open_row(col)
    board.drop_piece(row, col, HUMAN_PLAYER)
    change_turn() 
       
def play_AI_ply(board: CF.ConnectFour,  total_seconds: int) -> None:
    global start_time, total_time
    
    total_time, start_time = total_seconds, time.time()
    depth = 1
    max_depth_allowed = 100
    ply = None
    
    while depth < max_depth_allowed and not is_time_over(start_time, total_time):
        ply = DS.decision(board, AI_PLAYER, depth, ply)
        depth += 1
        
    print(f"Profundidad alcanzada: {depth - 1}\n")
    board.board = ply.board
    change_turn()
    
def is_goal_state(board: CF.ConnectFour, player: int) -> None:
    if board.test_win(player): BM.winning_game(player)
    elif board.test_tie(): BM.tied_game() 
    
def is_terminal(state: CF.ConnectFour) -> bool:
    return state.test_win(AI_PLAYER) or state.test_win(HUMAN_PLAYER) or state.test_tie()