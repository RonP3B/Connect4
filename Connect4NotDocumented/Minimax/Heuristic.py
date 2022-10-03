from Helpers import GameManagement as GM
from Classes import Class_ConnectFour as CF

def eval_space(piece: int, space: list) -> int:
    utility = 0
    opp_piece = (GM.HUMAN_PLAYER, GM.AI_PLAYER)[piece == GM.HUMAN_PLAYER]
    
    if space.count(piece) == 4: utility += 50
    elif space.count(piece) == 3 and space.count(0) == 1: utility += 6
    elif space.count(piece) == 2 and space.count(0) == 2: utility += 1
    if space.count(opp_piece) == 4: utility -= 50
    elif space.count(opp_piece) == 3 and space.count(0) == 1: utility -= 10 
    elif space.count(opp_piece) == 2 and space.count(0) == 2: utility -= 1
    
    return utility

def eval(board: CF.ConnectFour, piece: int) -> int:
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