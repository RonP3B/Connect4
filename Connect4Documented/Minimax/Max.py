# Librerias
import math

# Paquetes
from Helpers import GameManagement as GM
from Classes import Class_ConnectFour as CF
from Minimax import Min
from Minimax import Heuristic

def max_value(state: CF.ConnectFour, alpha: float, beta: float, piece: int, opp_piece: int, curr_depth: int = 0) -> tuple:  
    """
    Partiendo del estado recibido por parametro, retorna su estado hijo de mayor
    utilidad (valor)
    """
    
    # Si alcanzó el tiempo maximo retorna el caso de falla
    if GM.is_time_over(GM.start_time, GM.total_time): return GM.failed_case

    # Si el estado es terminal o si ya se alcanzo la profundidad dada         
    if  GM.is_terminal(state) or curr_depth == GM.max_depth: 
        
        # Se calcula la utilidad del estado con la heuristica y se retorna
        return (None, Heuristic.eval(state, piece))
    
    # Se inicializan con valores neutros las variables donde
    # se guardarán el estado y su utilidad
    maxChild, maxUtility = None, -math.inf 
    
    # Se expande el estado actual del juego con las jugadas del jugador   
    for child in state.expand(piece):
        
        # Se obtiene el estado hijo de 'child' de menor utilidad (_ = estado | utility = utilidad)
        _, utility = Min.min_value(child, alpha, beta, piece, opp_piece, curr_depth + 1) 
        
        # Si la utilidad que obtuvo es None significa que acabo el tiempo y en lugar de obtener
        # la evaluacion de la heuristica obtuvo el caso de fallo, por ende lo retornamos de nuevo
        # para acabar la funcion
        if utility == None: return GM.failed_case
           
        # Si la utilidad obtenida es mayor que la utilidad maxima actual   
        if utility > maxUtility: 
            
            # Se actualiza el estado actual y la utilidad maxima actual 
            maxChild, maxUtility = child, utility 
        
        # Si la utilidad maxima actual es mayor o igual a beta se usa un 'break' para detener
        # el bucle for y no recorrer los estados child que faltaban (o sea que se podan) 
        if maxUtility >= beta:
            break
        
        # Si la utilidad maxima actual es mayor que alpha
        if maxUtility > alpha:
            
            # Se actualiza el valor de alpha con la utilidad maxima actual
            alpha = maxUtility
            
    # Se retorna una tupla con el estado de mayor utiilidad junto al valor de su utilidad          
    return (maxChild, maxUtility)