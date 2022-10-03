# Librerias
import math

# Paquetes
from Helpers import GameManagement as GM
from Classes import Class_ConnectFour as CF
from Minimax import Max

def decision(state: CF.ConnectFour, piece: int, depth: int, last_ply: CF.ConnectFour) -> tuple:  
    """
    Obtiene el estado de juego con la mayor utilidad
    """
    
    # Se asigna la profundidad maxima elegida por el usuario
    GM.max_depth = depth
    
    # Se determina la ficha del oponente
    opp_piece = (GM.HUMAN_PLAYER, GM.AI_PLAYER)[piece == 1]
    
    # Se obtiene el mejor estado de juego, como la funcion 'max_value' devuelve
    # una tupla de 2 elementos se hace una destructuración: varA, varB = (valA, valB)
    # que es lo mismo que: varA = valA | varB = valB
    child, _ = Max.max_value(state, -math.inf, math.inf, piece, opp_piece)

    # Si obtuvo un estado de juego lo retorna, si no, significa que se acabo el tiempo
    # por ende se retorna la ultima jugada obtenida en el IDS
    return (last_ply, child)[child != None]