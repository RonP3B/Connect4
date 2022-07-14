"""
*Referenciado y modificado de: 
    https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
"""

# Librerias
import numpy as np  # Requiere instalación
import pygame  # Requiere instalación
import sys
import math


#***********************************Clase ConnectFour***********************************#
class ConnectFour():
    def __init__(self, rows: int, columns: int):
        # Se asignan las filas
        self.ROWS = rows
        
        # Se asignan las columnas
        self.COLUMNS = columns
        
        # Se inicializa una matriz de dimensión r * c con todos sus valores a 0 (tipo int)
        self.board = np.zeros((rows, columns), dtype = int)
    
    # Funcion para verificar si una columna ya está llena de 'fichas'
    def is_valid_location(self, col: int) -> bool:
        """
        Comprueba si en la columna seleccionada es posible jugar.     
        """
        
        # Si la primera fila de la columna esta vacía (es igual a 0) se puede
        # jugar en dicha columna, por lo tanto retorna true, si no, no esta vacía
        # y quiere decir que la columna ya esta llena por lo que no se puede jugar
        # en dicha columna y retorna false
        return self.board[0][col] == 0
    
    # Función para obtener la posición de la fila en la matriz donde se pondra la 'ficha'
    def get_next_open_row(self,col:int) -> bool:
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
    
    def test_goal(self, piece: int) -> bool:
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
    
    
    
    
#***********************************Variables globales***********************************#

# Colores RGB a utilizar para diseñar la GUI del tablero del juego
BLUE = (51, 51, 153)
WHITE = (237, 246, 249)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (230, 230, 0)

# Se crea el objeto de la clase ConnectFour
board = ConnectFour(6, 7)

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

# Variable para llevar un rastreo del turno de los jugadores(0: jugador uno, !0: jugador dos)
turn = 0

curr_piece_color = RED

# Inicializa todo los modulos de pygame
pygame.init()

# Fuente de texto que se usará en la etiqueta
myfont = pygame.font.SysFont("monospace", 75)




#***********************************Funciones globales***********************************#

# Función que diseña la ventana de pygame
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
            
            # Si la casilla actual tiene la ficha del jugador 1 dibuja el circulo rojo
            elif board.board[r][c] == 1:
                # Dibuja un circulo - (ventana, color, centro, radio)
                pygame.draw.circle(screen, RED, center, RADIUS)
            
            # La casilla actual tiene la ficha del jugador 2, se dibuja el circulo amarillo
            else:
                # Dibuja un circulo - (ventana, color, centro, radio)
                pygame.draw.circle(screen, YELLOW, center, RADIUS)
    
    # Actualiza la ventana pygame para que se reflejen los cambios            
    pygame.display.update()    
    
 
def draw_curr_piece(pos_x, color):
    # Posición central del circulo
    center = (pos_x, int(SQUARESIZE / 2))
    
    pygame.draw.circle(screen, color, center, RADIUS)
     
# Función que diseña el estado cuando un jugador gana
def winning_game(player: int) -> None:
    """
    Informa que jugador gano y finaliza el juego   
    """
    
    global game_over
    
    # Dibuja el tope de la ventana de blanco (para borrar la ficha del tope)
    pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
    
    #Si es el jugador uno escoge el rojo, si no el amarillo - (false,true)[condicion]
    color = (DARK_YELLOW, RED)[player == 1]
    
    # Etiqueta con el texto que indica el ganador
    label = myfont.render(f"Player {player} wins!", 1, color)
                        
    # Dibuja la etiqueta en la posicion dada de la ventana de pygame
    screen.blit(label, (25, 10))
                        
    # Termina el juego
    game_over = True
       
def play_ply(board, col, piece):
    """
    Juega el turno del jugador
    """
    
    global game_over, turn
    
    # Si la columna elegida no está llena realiza la jugada
    if board.is_valid_location(col):
                
        # Se obtiene la fila donde va a "caer la ficha"
        row = board.get_next_open_row(col)
                    
        # Se Rellena la posicion en el tablero con una ficha del jugador 1
        board.drop_piece(row, col, piece) 
                    
        # Si se conectaron cuatro fichas
        if board.test_goal(piece):
            winning_game(piece)
                    
        # Cambian los turnos (si el turno es igual a 0 cambia a 1 y viceversa) - (false,true)[condicion]   
        turn = (0, 1)[turn == 0]




#**************************************Metodo Main**************************************#

def main():
    global curr_piece_color
    
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

            # Si se mueve el mouse en la ventana de pygame
            if event.type == pygame.MOUSEMOTION:
                
                # Dibuja el tope de la ventana de blanco
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                
                # Obtiene la posicion en x-axis en la que se mueve el mouse
                posx = event.pos[0]
                
                # Se pinta la ficha del tope del color del jugador actual
                draw_curr_piece(posx, curr_piece_color)
            
            # Se actualiza la ventana para que se reflejen los cambios        
            pygame.display.update()

            # Si se clickea en la ventana de pygame
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # Posicion en el x-axis(como la x del plano cartesiano) donde se clickeó
                # o sea, la parte horizontal de la ventana donde el usuario dió click
                posX = event.pos[0]
                    
                # Se divide 'posX' entre el tamaño del cuadrado, esto para determinar que 
                # columna representa en la matriz la parte donde el usuario clickeó
                col = int(math.floor(posX / SQUARESIZE))

                #Turno del jugador uno
                if turn == 0:
                    # Se realiza la jugada del jugador 1
                    play_ply(board, col, 1)

                #Turno del jugador dos
                else:
                    # Se realiza la jugada del jugador 2
                    play_ply(board, col, 2)
                    
                # Si el turno es diferente de 0 la ficha del tope será amarilla, si no, roja    
                curr_piece_color = (RED, YELLOW)[turn != 0]
                
                # Si el juego no ha acabado se pinta la ficha del tope del color del jugador actual
                if not game_over: draw_curr_piece(posx, curr_piece_color)

                # Se vuelve a dibujar el tablero para que se reflejen los cambios
                draw_board(board)

                # Cuando el juego acabe, se hace una pausa de 4 segundos luego ya acaba la ejecución
                if game_over:
                    pygame.time.wait(4000)
                          
                                
if __name__ == '__main__':
    
    main()