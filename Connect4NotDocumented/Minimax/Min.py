import math
from Helpers import GameManagement as GM
from Classes import Class_ConnectFour as CF
from Minimax import Max
from Minimax import Heuristic

def min_value(state: CF.ConnectFour, alpha: float, beta: float, piece: int, opp_piece: int, curr_depth = 0) -> tuple:
    if GM.is_time_over(GM.start_time, GM.total_time): return GM.failed_case
         
    if GM.is_terminal(state) or curr_depth == GM.max_depth: return (None, Heuristic.eval(state, piece))

    minChild, minUtility = None, math.inf 
      
    for child in state.expand(opp_piece):
        _, utility = Max.max_value(child, alpha, beta, piece, opp_piece, curr_depth + 1)
    
        if utility == None: return GM.failed_case
                   
        if utility < minUtility: minChild, minUtility = child, utility

        if minUtility <= alpha: break
        
        if minUtility < beta: beta = minUtility
                         
    return (minChild, minUtility)
        