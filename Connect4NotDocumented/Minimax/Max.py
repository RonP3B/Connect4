import math
from Helpers import GameManagement as GM
from Classes import Class_ConnectFour as CF
from Minimax import Min
from Minimax import Heuristic

def max_value(state: CF.ConnectFour, alpha: float, beta: float, piece: int, opp_piece: int, curr_depth: int = 0) -> tuple:  
    if GM.is_time_over(GM.start_time, GM.total_time): return GM.failed_case
           
    if  GM.is_terminal(state) or curr_depth == GM.max_depth: return (None, Heuristic.eval(state, piece))
    
    maxChild, maxUtility = None, -math.inf 
     
    for child in state.expand(piece):
        _, utility = Min.min_value(child, alpha, beta, piece, opp_piece, curr_depth + 1) 

        if utility == None: return GM.failed_case
        
        if utility > maxUtility: maxChild, maxUtility = child, utility 
        
        if maxUtility >= beta: break
        
        if maxUtility > alpha: alpha = maxUtility
                   
    return (maxChild, maxUtility)