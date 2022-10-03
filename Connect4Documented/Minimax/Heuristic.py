# Paquetes
from Helpers import GameManagement as GM
from Classes import Class_ConnectFour as CF

def eval_space(piece: int, space: list) -> int:
    """
    Evalua la utilidad de un espacio de 4 según las fichas    
    """

    # Se inicializa la utilidad (prioridad) de un espacio de 4
    utility = 0
    
    # Se determina la ficha del oponente - (False, True)[condicion]
    opp_piece = (GM.HUMAN_PLAYER, GM.AI_PLAYER)[piece == GM.HUMAN_PLAYER]
    
    # Si hay 4 fichas 'piece' conectadas en el espacio
    if space.count(piece) == 4:
        
        # Se suma un numero grande para que el estado sea el de mas prioridad 
        utility += 50
    
    # Si hay 3 fichas 'piece' en el espacio y un espacio vacío
    elif space.count(piece) == 3 and space.count(0) == 1:
        utility += 6
        
    # Si hay 2 fichas 'piece' en el espacio y dos espacios vacíos
    elif space.count(piece) == 2 and space.count(0) == 2:
        utility += 1
               
    
    # Si hay 4 fichas del oponente conectadas en el espacio
    if space.count(opp_piece) == 4:
        
        # Se resta un numero grande porque es un estado donde se pierde 
        utility -= 50
    
    # Si hay 3 fichas del oponente en el espacio y un espacio vacío
    elif space.count(opp_piece) == 3 and space.count(0) == 1:
        utility -= 10 
    
    # Si hay 2 fichas del oponente en el espacio y dos espacios vacíos
    elif space.count(opp_piece) == 2 and space.count(0) == 2:
        utility -= 1
    
    return utility

def eval(board: CF.ConnectFour, piece: int) -> int:
    """
    Heuristica para evaluar la utilidad del estado pasado por parametro
    """
    
    # Se inicializa la utilidad (prioridad) de un estado del juego
    utility = 0
    
    # Cada ficha en el centro es un bonus de 3 puntos, ya que jugar en el
    # centro da mas posibilidades de ganar. Esto: [i for i in board.board[:,board.COLUMNS // 2]]
    # genera una lista con todas las filas de la columna del medio
    centerColumn = [i for i in board.board[:,board.COLUMNS // 2]]
    
    # Se suman 3 puntos por cada ficha 'piece' en el medio
    utility += centerColumn.count(piece) * 3

    # Se evalua cada espacio de 4 en horizontal del tablero
    # (Documentación en función 'check_all_horizontals' de la clase ConnectFour)
    for r in range(board.ROWS): 
        for c in range(board.COLUMNS - 3):
            
            # Se obtiene el espacio de 4 a evaluar
            current_space = list(board.board[r][c:c + 4])
        
            # Se evalua el espacio y se suma su resultado
            utility += eval_space(piece, current_space)
     
     
    # Se evalua cada espacio de 4 en vertical del tablero
    # (Documentación en función 'check_all_verticals' de la clase ConnectFour)       
    for c in range(board.COLUMNS):
        for r in range(board.ROWS - 3):
            
            # Se obtiene el espacio de 4 a evaluar
            current_space = list(board.board[r:r + 4, c])
            
            # Se evalua el espacio y se suma su resultado
            utility += eval_space(piece, current_space)
            
    # Se evalua cada espacio de 4 en diagonal del tablero
    # (Documentación en función 'check_all_diagonals' de la clase ConnectFour) 
    for c in range(board.COLUMNS - 3):
        for r in range(board.ROWS - 3): 
            
            # Se obtiene el espacio de 4 a evaluar
            current_space = [board.board[r+x][c+x] for x in range(4)]
            
            # Se evalua el espacio y se suma su resultado
            utility += eval_space(piece, current_space)    
    
    # Se evalua cada espacio de 4 en diagonal negativa del tablero
    # (Documentación en función 'check_all_diagonals' de la clase ConnectFour)    
    for c in range(board.COLUMNS - 3):
        for r in range(3, board.ROWS):
            
            # Se obtiene el espacio de 4 a evaluar
            current_space = [board.board[r-x][c+x] for x in range(4)]
            
            # Se evalua el espacio y se suma su resultado
            utility += eval_space(piece, current_space)
            
    # Se retorna la ultilidad total del estado
    return utility