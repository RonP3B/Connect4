import math
from Helpers import GameManagement as GM
from Classes import Class_ConnectFour as CF
from Minimax import Max

def decision(state: CF.ConnectFour, piece: int, depth: int, last_ply: CF.ConnectFour) -> tuple:  
    GM.max_depth = depth
    opp_piece = (GM.HUMAN_PLAYER, GM.AI_PLAYER)[piece == 1]
    child, _ = Max.max_value(state, -math.inf, math.inf, piece, opp_piece)
    return (last_ply, child)[child != None]