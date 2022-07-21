# Librerias
import numpy as np  # Requiere instalación
import pygame  # Requiere instalación
import sys
import math
import copy

#***********************************Clase ConnectFour***********************************#
class ConnectFour():
    def __init__(self, board: list, rows: int, columns: int, parent = None):
        # Se asignan el numero de filas pasado al crear el objeto
        self.ROWS = rows
        
        # Se asignan numero de columnas pasado al crear el objeto
        self.COLUMNS = columns
        
        # Se asigna el borde pasado al crear el objeto
        self.board = board
        
    def is_valid_location(self, col: int) -> bool:
        """
        Comprueba si en la columna seleccionada es posible jugar.     
        """
        
        # Si la primera fila de la columna esta vacía (es igual a 0) se puede
        # jugar en dicha columna, por lo tanto retorna true, si no, no esta vacía
        # y quiere decir que la columna ya esta llena por lo que no se puede jugar
        # en dicha columna y retorna false
        return self.board[0][col] == 0
    
    def get_next_open_row(self,col:int) -> int:
        """
        Determina la fila de la columna pasada por parametro en donde va a caer la ficha.
        """
        
        # Bucle para recorrer las filas de la columna pasada por parametro empezando
        # desde la fila del fondo (bottom - top)
        for r in range(self.ROWS -1, -1, -1):
            
            # Si la fila actual está vacía (es igual a 0) es donde debe caer la 'ficha'
            if self.board[r][col] == 0: 
                
                # Retornamos dicha fila
                return r
    
    def drop_piece(self, row: int, col: int, piece: int) -> None:
        """
        Inserta la ficha en la posición indicada
        """
        
        self.board[row][col] = piece
            
    def check_all_horizontals(self, four_connected: list) -> bool:
        """
        Revisa todas las posiciones donde es posible que se concecten 4 fichas
        de manera horizontal en busca de si hay 4 fichas conectadas horizontalmente
        
        Retorna:
            True: Si hay 4 fichas conectadas horizontalmente
            False: Si no hay 4 fichas conectadas horizontalmente
        """
        
        # Bucle que verifica todos los espacios donde se puede ganar de manera horizontal
        # funciona de la siguiente manera(fijate en los espacios encerrados entre comillas):
        #
        # [ 0 0 0 0  0 0 0]     [0  0 0 0 0  0 0]     [0 0  0 0 0 0  0]     [0 0 0  0 0 0 0 ]
        # [ 0 0 0 0  0 0 0]     [0  0 0 0 0  0 0]     [0 0  0 0 0 0  0]     [0 0 0  0 0 0 0 ]
        # [ 0 0 0 0  0 0 0]  => [0  0 0 0 0  0 0]  => [0 0  0 0 0 0  0]  => [0 0 0  0 0 0 0 ]
        # [ 0 0 0 0  0 0 0]     [0  0 0 0 0  0 0]     [0 0  0 0 0 0  0]     [0 0 0  0 0 0 0 ]
        # [ 0 0 0 0  0 0 0]     [0  0 0 0 0  0 0]     [0 0  0 0 0 0  0]     [0 0 0  0 0 0 0 ]
        # ['0 0 0 0' 0 0 0]     [0 '0 0 0 0' 0 0]     [0 0 '0 0 0 0' 0]     [0 0 0 '0 0 0 0']
        #
        # Y de esa manera continua con las demás filas de arriba que faltan por ver, si en el espacio
        # revisado todos los numeros son igual al parametro 'piece' es que hay 4 fichas conectadas
        for r in range(self.ROWS):
            
            # Se le resta 3 a las columnas ya que no hace falta recorrer las tres ultimas columnas 
            for c in range(self.COLUMNS - 3):
                
                # El 'board[r][c:c + 4] ***board[fila][columnaInicial:columnaFinal]***' 
                # ([r]-fila actual | [c:c + 4]-de la columna actual a las 3 columnas siguientes)
                # esto genera una lista con los 4 espacios a ser revisados, si dicha lista es igual a la 
                # lista 'four_connected' (se usa la funcion 'all()' para tomar en cuenta que todos
                # los valores de ambas listas sean iguales) se retornará true y acaba la función                
                if (self.board[r][c:c + 4] == four_connected).all(): 
                    return True
                
        # Si no hay 4 fichas conectadas en ningún espacio horizontal se retorna falso
        return False
    
    def check_all_verticals(self, four_connected:list) -> bool:
        """
        Revisa todas las posiciones donde es posible que se concecten 4 fichas
        de manera vertical en busca de si hay 4 fichas conectadas verticalmente.
        
        Retorna:
            True: Si hay 4 fichas conectadas verticalmente
            False: Si no hay 4 fichas conectadas verticalmente
        """

        # Bucle que verifica todos los espacios donde se puede ganar de manera vertical
        # funciona de la siguiente manera(fijate en los espacios encerrados entre ||):
        #
        # [ 0  0 0 0 0 0 0]     [ 0  0 0 0 0 0 0]     [|0| 0 0 0 0 0 0]     
        # [ 0  0 0 0 0 0 0]     [|0| 0 0 0 0 0 0]     [|0| 0 0 0 0 0 0]     
        # [|0| 0 0 0 0 0 0]  => [|0| 0 0 0 0 0 0]  => [|0| 0 0 0 0 0 0]  
        # [|0| 0 0 0 0 0 0]     [|0| 0 0 0 0 0 0]     [|0| 0 0 0 0 0 0]     
        # [|0| 0 0 0 0 0 0]     [|0| 0 0 0 0 0 0]     [ 0  0 0 0 0 0 0]     
        # [|0| 0 0 0 0 0 0]     [ 0  0 0 0 0 0 0]     [ 0  0 0 0 0 0 0]  
        #
        # Y de esa manera continua con las columnas que faltan por ver, si en el espacio
        # revisado todos los numeros son igual al parametro 'piece' es que hay 4 fichas conectadas
        for c in range(self.COLUMNS):
            
            # Se le resta 3 a las filas ya que no hace falta recorrer las tres ultimas filas
            for r in range(self.ROWS - 3):
                
                # El 'board[r:r+4,c] ***board[filaInicial:FilaFinal, columna]***' 
                # ('r:r+4' - desde la fila actual a las 3 filas siguientes | c - columna actual)
                # esto genera una lista con los 4 espacios a ser revisados, si dicha lista es igual a la 
                # lista 'four_connected' (se usa la funcion 'all()' para tomar en cuenta que todos
                # los valores de ambas listas sean iguales) se retornará true y acaba la función
                if (self.board[r:r+4,c] == four_connected).all():
                    return True
                
        # Si no hay 4 fichas conectadas en ningún espacio vertical se retorna falso
        return False
    
    def check_all_diagonals(self, four_connected:list) -> bool:     
        """
        Revisa todas las posiciones donde es posible que se concecten 4 fichas
        de manera diagonal en busca de si hay 4 fichas conectadas diagonalmente.
        
        Retorna:
            True: Si hay 4 fichas conectadas diagonalmente
            False: Si no hay 4 fichas conectadas diagonalmente
        """
        
        # Bucle que verifica todos los espacios donde se puede ganar de manera diagonal
        # funciona de la siguiente manera(fijate en los espacios encerrados en ||):
        #
        # [ 0  0  0  0  0 0 0]     [ 0  0  0  0  0 0 0]     [ 0  0  0 |0| 0 0 0]     
        # [ 0  0  0  0  0 0 0]     [ 0  0  0 |0| 0 0 0]     [ 0  0 |0| 0  0 0 0]     
        # [ 0  0  0 |0| 0 0 0]  => [ 0  0 |0| 0  0 0 0]  => [ 0 |0| 0  0  0 0 0]  
        # [ 0  0 |0| 0  0 0 0]     [ 0 |0| 0  0  0 0 0]     [|0| 0  0  0  0 0 0]     
        # [ 0 |0| 0  0  0 0 0]     [|0| 0  0  0  0 0 0]     [ 0  0  0  0  0 0 0]     
        # [|0| 0  0  0  0 0 0]     [ 0  0  0  0  0 0 0]     [ 0  0  0  0  0 0 0]     
        #
        # Y de esa manera continua, con las demás columnas de, si en el espacio revisado todos
        # los numeros son igual al parametro 'piece' es que hay 4 fichas conectadas diagonalmente
        
        # Se le resta 3 a las columnas ya que no hace falta recorrer las tres ultimas columnas
        for c in range(self.COLUMNS - 3):
            
            # Se le resta 3 a las filas ya que no hace falta recorrer las tres ultimas filas
            for r in range(self.ROWS - 3): 
                
                # El '[board[r+x][c+x] for x in range(4)]' genera una lista que partiendo de 
                # la fila y columna actuales obtiene 4 espacios más diagonalmente en la matriz, si
                # dicha lista es igual a 'four_connected' se retornará true y acaba la función        
                if ([self.board[r+x][c+x] for x in range(4)] == four_connected):
                    return True
                
        # Si no hay 4 fichas conectadas en ningún espacio diagonal se retorna falso
        return False
    
    def check_all_negative_diagonals(self, four_connected:list) -> bool:
        """
        Revisa todas las posiciones donde es posible que se concecten 4 fichas de manera 
        diagonal negativa en busca de si hay 4 fichas conectadas diagonalmente
        
        Retorna:
            True: Si hay 4 fichas conectadas diagonalmente
            False: Si no hay 4 fichas conectadas diagonalmente
        """
        
        # Bucle que verifica todos los espacios donde se puede ganar de manera diagonal negativa
        # funciona de la siguiente manera(fijate en los espacios encerrados en ||):
        #
        # [ 0   0   0   0  0 0 0]     [ 0   0   0   0  0 0 0]     [|0|  0   0   0  0 0 0]     
        # [ 0   0   0   0  0 0 0]     [|0|  0   0   0  0 0 0]     [ 0  |0|  0   0  0 0 0]     
        # [|0|  0   0   0  0 0 0]  => [ 0  |0|  0   0  0 0 0]  => [ 0   0  |0|  0  0 0 0]  
        # [ 0  |0|  0   0  0 0 0]     [ 0   0  |0|  0  0 0 0]     [ 0   0   0  |0| 0 0 0]     
        # [ 0   0  |0|  0  0 0 0]     [ 0   0   0  |0| 0 0 0]     [ 0   0   0   0  0 0 0]     
        # [ 0   0   0  |0| 0 0 0]     [ 0   0   0   0  0 0 0]     [ 0   0   0   0  0 0 0]     
        #
        # Y de esa manera continua, con las demás columnas, si en el espacio revisado todos
        # los numeros son igual al parametro 'piece' es que hay 4 fichas conectadas diagonalmente
        
        # Se le resta 3 a las columnas ya que no hace falta recorrer las tres ultimas columnas
        for c in range(self.COLUMNS - 3):
            
            # Se empieza de la cuarta fila hasta la ultima(la sexta), esto porque debajo de la cuarta
            #fila no se conectan 4 diagonalmente, solo 3, por lo que no es necesario revisarlas
            for r in range(3, self.ROWS):
            
                # El '[board[r-x][c+x] for x in range(4)]' genera una lista en la que partiendo de 
                # la fila y columna actuales obtiene 4 espacios más diagonalmente hacia abajo en la
                # matriz, si dicha lista es igual a 'four_connected' se retornará true y acaba la función 
                if [self.board[r-x][c+x] for x in range(4)] == four_connected:
                    return True
        
        # Si no hay 4 fichas conectadas en ningún espacio diagonal negativo se retorna falso
        return False
    
    def expand(self, player: int) -> list:
        """
        Genera una lista de objetos tipo ConnectFour con todas las jugadas posibles del 
        jugador pasado por parametro que se pueden realizar a partir del objeto actual
        """
        
        # Lista donde se guardarán los estados de juegos creados al expandirse
        children = []
        
        # Bucle para recorrer cada columna
        for col in range(self.COLUMNS):
            
            # Se verifica si la columna es valida para 'ingresar una ficha'
            if self.is_valid_location(col):
                
                # Se obtiene donde 'caera la ficha'
                nextOpenRow = self.get_next_open_row(col)
                
                # Se crea un objeto de la clase ConnectFour que replica al objeto actual
                newChild = ConnectFour(copy.copy(self.board), self.ROWS, self.COLUMNS, self) 
                
                # Se realiza la jugada en el nuevo objeto
                newChild.drop_piece(nextOpenRow, col, player)
                
                # Se guarda el objeto con la jugada realizada en la lista children
                children.append(newChild)
        
        # Se retorna la lista con los objetos que representan todas las jugadas posibles
        return children
                
    
    def test_win(self, piece: int) -> bool:
        """
        Verifica si en el tablero ya se conectaron 4 fichas
        """

        # Genera una lista de 4 elementos, dichos elementos tendran todos el valor del
        # parametro 'piece', el cual es el numero que representa la ficha del jugador
        four_connected = [piece for i in range(4)]
        
        # Se verifican todas las casillas(posiciones) donde se pueden conectar 4 'fichas'
        # si en una se cumple, retorna true y termina la función
        if self.check_all_horizontals(four_connected): return True
        if self.check_all_verticals(four_connected): return True
        if self.check_all_diagonals(four_connected): return True
        if self.check_all_negative_diagonals(four_connected): return True
        
        # Se retorna false si no hay 4 fichas conectadas en el tablero
        return False
    
    def test_tie(self) -> bool:
        """
        Verifica si el juego quedo empate
        """
        
        # Si alguna columna no está llena se retorna falso y la funcion termina
        for col in range(self.COLUMNS):
            if self.is_valid_location(col):
                return False
        
        # Se retorna true si todas las columnas estan llenas
        return True
    
    
    
#***********************************Variables globales***********************************#

# Colores RGB a utilizar para diseñar la GUI del tablero del juego
BLUE = (51, 51, 153)
WHITE = (237, 246, 249)
RED = (255, 0, 0)
YELLOW = (255, 235, 10)
DARK_YELLOW = (230, 230, 0)

# Se crea el objeto de la clase ConnectFour
board = ConnectFour(np.zeros((6, 7), dtype=int), 6, 7)

# Tamaño de los cuadrados que representan cada fila y columna en el tablero
SQUARESIZE = 100

# El ancho de la ventana será igual al producto del numero de 
# columnas en nuestro tablero por el tamaño del cuadrado
width = board.COLUMNS * SQUARESIZE

# El alto de la ventana será igual al del numero de filas en el tablero
# (se le agrega una fila más para el espacio donde se mueve la ficha)
# multiplicado por el tamaño del cuadrado
height = (board.ROWS + 1) * SQUARESIZE

# Se asigna el tamaño de la ventana
size = (width, height)

# Se crea una ventana de pygame con el tamaño de la variable 'size' 
screen = pygame.display.set_mode(size)

# Radio que determinara el tamaño de los circulos
RADIUS = int(SQUARESIZE / 2 - 7) 

# Variable para llevar un rastreo de que si el juego ha acabado o no
game_over = False

# Se asigna el valor de los jugadores (1: jugador, 2: IA)
HUMAN_PLAYER, AI_PLAYER = 1, 2

# Variable para llevar un rastreo del turno (Empieza la AI)
turn = AI_PLAYER

# Inicializa todo los modulos de pygame
pygame.init()

# Fuente de texto que se usará en la etiqueta
myfont = pygame.font.SysFont("monospace", 75)


#***********************************Funciones globales***********************************#

def draw_board(board: ConnectFour) -> None:
    """
    Dibuja la representación del tablero pasado por parametro en la ventana
    de pygame
    """

    # Bucle que dibuja todos los cuadrados de la ventana de pygame de azul con un 
    # circulo en el medio (el color del circulo depende si hay ficha o esta vacio),
    # esto para representar el 'board'(el tablero) graficamente
    for c in range(board.COLUMNS):  
        for r in range(board.ROWS):
            
            # Rectangulo que representa el tablero - (pos-X, pos-Y, size-X, size-Y)
            board_rec = (c * SQUARESIZE, (r * SQUARESIZE) + SQUARESIZE, SQUARESIZE, SQUARESIZE)
            
            # Posición donde del centro del circulo dentro de los rectangulos
            center = (int((c * SQUARESIZE) + (SQUARESIZE / 2)), int((r * SQUARESIZE) + (SQUARESIZE / 2) + SQUARESIZE))
            
            # Dibuja un rectangulo - (ventana, color, rectangulo)
            pygame.draw.rect(screen, BLUE, board_rec)
            
            # Si la casilla actual está vacia dibuja el circulo blanco
            if board.board[r][c] == 0:
                # Dibuja un circulo - (ventana, color, centro, radio)
                pygame.draw.circle(screen, WHITE, center, RADIUS)
            
            # Si la casilla actual tiene la ficha del jugador dibuja el circulo rojo
            elif board.board[r][c] == 1:
                # Dibuja un circulo - (ventana, color, centro, radio)
                pygame.draw.circle(screen, RED, center, RADIUS)
            
            # La casilla actual tiene la ficha de la IA, se dibuja el circulo amarillo
            else:
                # Dibuja un circulo - (ventana, color, centro, radio)
                pygame.draw.circle(screen, YELLOW, center, RADIUS)
    
    # Actualiza la ventana pygame para que se reflejen los cambios            
    pygame.display.update()    

def remove_piece_from_top() -> None:
    """
    Borra la ficha que está en el tope de la ventana
    """
    
    # Dibuja el tope de la ventana de blanco (para borrar la ficha del tope)
    pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
    
    # Se actualiza la ventana para que se refleje los cambios        
    pygame.display.update()
     
def winning_game(player: int) -> None:
    """
    Diseña el mensaje de que jugador gano y finaliza el juego   
    """
    
    # Se elimina la ficha del tope para mostrar el mensaje
    remove_piece_from_top()
    
    # Si es el jugador humano escoge el rojo, si es la AI el amarillo
    color = (DARK_YELLOW, RED)[player == HUMAN_PLAYER]
    
    # Mensaje que será mostrado dependiendo el ganador
    msg = ("The AI beat you", "You have won!!!")[player == HUMAN_PLAYER]
    
    # Se crea la etiqueta con el texto que indica el ganador
    label = myfont.render(msg, 1, color)
                        
    # Dibuja la etiqueta en la posicion dada de la ventana de pygame
    screen.blit(label, (20, 10))
                        
    end_game()
    
def tied_game() -> None:
    """
    Diseña el mensaje de que el juego ha quedado empate y finaliza el juego   
    """ 
    
    # Se elimina la ficha del tope para mostrar el mensaje
    remove_piece_from_top()
            
    # Etiqueta con el texto que indica el ganador
    label = myfont.render(f"Game tied", 1, BLUE)
                                
    # Dibuja la etiqueta en la posicion dada de la ventana de pygame
    screen.blit(label, (150, 10))
    
    # Finaliza el juego                            
    end_game()
    
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
    
  
def play_human_ply(board: ConnectFour, col: int) -> None:
    """
    Realiza la jugada del usuario
    """
    
    # Se obtiene la fila donde va a "caer la ficha"
    row = board.get_next_open_row(col)
                        
    # Se Rellena la posicion en el tablero con una ficha del jugador
    board.drop_piece(row, col, HUMAN_PLAYER)
    
    # Se cambian los turnos
    change_turn() 
       
def play_AI_ply(board: ConnectFour, depth: int):
    """
    Juega el turno de la AI aplicando el algoritmo minimax con podado
    alpha beta a una profundidad limitada según el parametro 'depth'.
    """
    
    # Se decide y se obtiene el mejor estado de juego
    ply = decision(board, AI_PLAYER, depth)
    
    # Se cambia el tablero actual por el tablero obtenido que contiene la
    # jugada de la AI
    board.board = ply.board
    
    # Se cambian los turnos
    change_turn()
    
def is_goal_state(board: ConnectFour, player: int) -> None:
    """
    Verifica si el jugador obtenido por parametro ha ganado
    o si el juego ha finalizado
    """

    # Se verifica si el jugador inidcado ha ganado 
    if board.test_win(player):
        
        # Se informa que ha ganado y se finaliza el juego        
        winning_game(player)

    # Sino, Se verifica si el juego ha quedado empate
    elif board.test_tie():
        
        # Se informa que ha quedado empate y se finaliza el juego 
        tied_game() 
    
#********************************MINIMAX CON ALPHA BETA PRUNING********************************#

# Variable global en la que se asignará la profundidad maxima a la que llegará el algoritmo
max_depth = 0

def is_terminal(state: ConnectFour) -> bool:
    """
    Verifica si el estado es terminal, esto mirando si algún jugador ganó
    o si el juego quedó empate
    """
    
    # Si la AI ganó o si el humano ganó o si quedo empate retorna True porque es terminal
    return state.test_win(AI_PLAYER) or state.test_win(HUMAN_PLAYER) or state.test_tie()
    
def min_value(state, alpha, beta, piece, opp_piece, curr_depth = 0) -> tuple:
    """
    Partiendo del estado recibido por parametro, retorna su estado hijo de menor
    utilidad (valor)
    """
    
    # Si el estado es terminal o si ya se alcanzo la profundidad dada      
    if is_terminal(state) or curr_depth == max_depth: 
        
        # Se calcula la utilidad del estado con la heuristica y se retorna
        return (None, eval(state, piece))
    
    # Se inicializan con valores neutros las variables donde
    # se guardarán el estado y su utilidad 
    minChild, minUtility = None, math.inf 
    
    # Se expande el estado actual del juego con las jugadas del oponente   
    for child in state.expand(opp_piece):
        
        # Se obtiene el estado hijo de 'child' de mayor utilidad (_ = estado | utility = utilidad)
        _, utility = max_value(child, alpha, beta, piece, opp_piece, curr_depth + 1)
        
        # Si la utilidad obtenida es menor que la utilidad minima actual               
        if utility < minUtility:
            
            # Se actualiza el estado actual y la utilidad minima actual 
            minChild, minUtility = child, utility
        
        # Si la utilidad minima actual es menor o igual a alpha se usa un 'break' para detener
        # el bucle for y no recorrer los estados child que faltaban (o sea que se podan) 
        if minUtility <= alpha: 
            break
            
        # Si la utilidad minima actual es menor que beta
        if minUtility < beta:
            
            # Se actualiza el valor de beta con la utilidad minima actual
            beta = minUtility
    
    # Se retorna una tupla con el estado de menor utiilidad junto al valor de su utilidad                  
    return (minChild, minUtility)
        
def max_value(state: ConnectFour, alpha, beta, piece: int, opp_piece: int, curr_depth: int = 0) -> tuple:  
    """
    Partiendo del estado recibido por parametro, retorna su estado hijo de mayor
    utilidad (valor)
    """

    # Si el estado es terminal o si ya se alcanzo la profundidad dada         
    if  is_terminal(state) or curr_depth == max_depth: 
        
        # Se calcula la utilidad del estado con la heuristica y se retorna
        return (None, eval(state, piece))
    
    # Se inicializan con valores neutros las variables donde
    # se guardarán el estado y su utilidad
    maxChild, maxUtility = None, -math.inf 
    
    # Se expande el estado actual del juego con las jugadas del jugador   
    for child in state.expand(piece):
        
        # Se obtiene el estado hijo de 'child' de menor utilidad (_ = estado | utility = utilidad)
        _, utility = min_value(child, alpha, beta, piece, opp_piece, curr_depth + 1) 
           
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

def decision(state: ConnectFour, piece: int, depth: int) -> ConnectFour:  
    """
    Obtiene el estado de juego con la mayor utilidad
    """
    
    # Se referencia la variable que determinará la profundida maxima    
    global max_depth 
    
    # Se asigna la profundidad maxima elegida por el usuario
    max_depth = depth
    
    # Se determina la ficha del oponente
    opp_piece = (HUMAN_PLAYER, AI_PLAYER)[piece == 1]
    
    # Se obtiene el mejor estado de juego, como la funcion 'max_value' devuelve
    # una tupla de 2 elementos se hace una destructuración: varA, varB = (valA, valB)
    # que es lo mismo que: varA = valA | varB = valB
    child, _ = max_value(state, -math.inf, math.inf, piece, opp_piece)

    # Se retorna el estado de juego obtenido
    return child
    
def eval_space(piece: ConnectFour, space: int) -> int:
    """
    Evalua la utilidad de un espacio de 4 según las fichas    
    """

    # Se inicializa la utilidad (prioridad) de un espacio de 4
    utility = 0
    
    # Se determina la ficha del oponente - (False, True)[condicion]
    opp_piece = (HUMAN_PLAYER, AI_PLAYER)[piece == HUMAN_PLAYER]
    
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

def eval(board: ConnectFour, piece: int) -> int:
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


#**************************************Metodo Main**************************************#

def main():
    global turn
        
    # Dibuja el diseño del tablero en la ventana de pygame
    draw_board(board)
    
    #Bucle que correrá siempre y cuando el juego no se haya terminado,
    #la variable 'game_over' es booleana, como hay una negación (el not)
    #se entrará en el bucle cuando 'game_over' sea falso
    while not game_over:
        
        # Bucle que sirve para capturar todos los eventos que suceden en la
        # ventana de pygame
        for event in pygame.event.get():
            
            #Si se presiona el botón de cerrar de la ventana de pygame
            if event.type == pygame.QUIT:
                #Cierra la ventana y acaba la ejecución del programa
                sys.exit()

            # Si se mueve el mouse en la ventana de pygame en el turno del jugador
            if event.type == pygame.MOUSEMOTION and turn == HUMAN_PLAYER:
                # Dibuja el tope de la ventana de blanco
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                
                # Obtiene la posicion en x-axis en la que se mueve el mouse
                posX = event.pos[0]
                
                # Posición central del circulo
                center = (posX, int(SQUARESIZE / 2))
    
                pygame.draw.circle(screen, RED, center, RADIUS)
            
            # Se actualiza la ventana para que se reflejen los cambios        
            pygame.display.update()

            # Si se clickea en la ventana de pygame en el turno del jugador
            if event.type == pygame.MOUSEBUTTONDOWN and turn == HUMAN_PLAYER:
                
                # Posicion en el x-axis(como la x del plano cartesiano) donde se clickeó
                # o sea, la parte horizontal de la ventana donde el usuario dió click
                posX = event.pos[0]
                    
                # Se divide 'posX' entre el tamaño del cuadrado, esto para determinar que 
                # columna representa en la matriz la parte donde el usuario clickeó
                col = int(math.floor(posX / SQUARESIZE))
                
                # Si la columna elegida no está llena realiza la jugada
                if board.is_valid_location(col):
                    
                    # Se realiza la jugada del humano
                    play_human_ply(board, col)
                    
                    # Se verifica si el humano ganó el juego o quedo si quedó empate
                    is_goal_state(board, HUMAN_PLAYER)
                        
                    # Se vuelve a dibujar el tablero para que se reflejen los cambios
                    draw_board(board)

        # Turno de la IA
        if turn == AI_PLAYER and not game_over:
            # Se borra la ficha del jugador humano
            remove_piece_from_top()
            
            # Se juega el turno de la AI
            play_AI_ply(board, 4)
        
            # Se verifica si la AI ganó el juego o si quedó empate
            is_goal_state(board, AI_PLAYER)
            
            # Se vuelve a dibujar el tablero para que se reflejen los cambios
            draw_board(board)
             
        # Sí el juego ha finalizado
        if game_over: 
            
            # Se hace una pausa de 7 segundos para que se pueda apreciar el resultado
            # y luego ya acaba la ejecución
            pygame.time.wait(7000)
                                       
if __name__ == '__main__':
    main()