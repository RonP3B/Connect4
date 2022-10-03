# Librerias
import time

# Paquetes
from Classes import Class_ConnectFour as CF
from Helpers import BoardManagement as BM
from Minimax import Desicion as DS

# Variable para llevar un rastreo de que si el juego ha acabado o no
game_over = False

# Se asigna el valor de los jugadores (1: jugador, 2: IA)
HUMAN_PLAYER, AI_PLAYER = 1, 2

# Para llevar rastreo del tiempo del IDS
start_time = total_time = 0

# En caso de que alcanze el tiempo maximo y tenga que detener la función 
failed_case = (None, None)

# Variable global en la que se asignará la profundidad maxima a la que llegará el algoritmo
max_depth = 0 

# Variable para llevar un rastreo del turno (Empieza la AI)
turn = 2 #AI_PLAYER

def end_game() -> None:
    """
    Finaliza la ejecución del juego
    """
    
    # Se referencia la variable global que rastrea si el juego continua 
    global game_over
    
    # Se indica que el juego ha finalizado
    game_over = True

def change_turn() -> None:
    """
    Cambia el turno de los jugadores
    """
    
    # Se referencia la variable global que rastrea los turnos
    global turn
    
    # Cambian los turnos (si es el turno del humano cambia al de la AI y viceversa)   
    turn = (HUMAN_PLAYER, AI_PLAYER)[turn == HUMAN_PLAYER]
    

def is_time_over(start_time: float, total_time: float) -> bool:
    """
    Verifica si el tiempo total ha acabado
    """
    # 'time.time() - start_time' obtiene los segundos que han pasado
    return time.time() - start_time >= total_time
  
def play_human_ply(board: CF.ConnectFour, col: int) -> None:
    """
    Realiza la jugada del usuario
    """
    
    # Se obtiene la fila donde va a "caer la ficha"
    row = board.get_next_open_row(col)
                        
    # Se Rellena la posicion en el tablero con una ficha del jugador
    board.drop_piece(row, col, HUMAN_PLAYER)
    
    # Se cambian los turnos
    change_turn() 
       
def play_AI_ply(board: CF.ConnectFour,  total_seconds: int):
    """
    Juega el turno de la AI aplicando el algoritmo minimax con podado
    alpha beta mediante un IDS limitado por los segundos especificados.
    """
    global start_time, total_time
    
    #Variables para llevar un rastreo del tiempo
    total_time, start_time = total_seconds, time.time()
    
    # Profundidad inicial
    depth = 1
    
    # Profundidad maxima permitida
    max_depth_allowed = 100
    
    # Variable que almacenará la mejor jugada
    ply = None
    
    # bucle que aplica el IDS, se ejecuta si no se ha alcanzado la profundidad
    # maxima permitida Y si el tiempo dado no ha acabado.
    while depth < max_depth_allowed and not is_time_over(start_time, total_time):
        
        # Se obtiene el mejor estado de juego dentro de la profundidad actual
        ply = DS.decision(board, AI_PLAYER, depth, ply)
        
        # Se aumenta la profundidad actual
        depth += 1
       
    # Informa la profundidad alcanzada
    print(f"Profundidad alcanzada: {depth - 1}\n")
    
    # Se cambia el tablero actual por el tablero obtenido que contiene la
    # jugada de la AI
    board.board = ply.board
    
    # Se cambian los turnos
    change_turn()
    
def is_goal_state(board: CF.ConnectFour, player: int) -> None:
    """
    Verifica si el jugador obtenido por parametro ha ganado
    o si el juego ha finalizado
    """

    # Se verifica si el jugador inidcado ha ganado 
    if board.test_win(player):
        
        # Se informa que ha ganado y se finaliza el juego        
        BM.winning_game(player)

    # Sino, Se verifica si el juego ha quedado empate
    elif board.test_tie():
        
        # Se informa que ha quedado empate y se finaliza el juego 
        BM.tied_game() 
    
def is_terminal(state: CF.ConnectFour) -> bool:
    """
    Verifica si el estado es terminal, esto mirando si algún jugador ganó
    o si el juego quedó empate
    """
    
    # Si la AI ganó o si el humano ganó o si quedo empate retorna True porque es terminal
    return state.test_win(AI_PLAYER) or state.test_win(HUMAN_PLAYER) or state.test_tie()