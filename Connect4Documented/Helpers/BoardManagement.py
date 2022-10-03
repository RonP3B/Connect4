# Librerias
import numpy as np  # Requiere instalación
import pygame 

# Paquetes
from Classes import Class_ConnectFour as CF
from Helpers import GameManagement as GM

# Colores RGB a utilizar para diseñar la GUI del tablero del juego
BLUE = (51, 51, 153)
WHITE = (237, 246, 249)
RED = (255, 0, 0)
YELLOW = (255, 235, 10)
DARK_YELLOW = (230, 230, 0)

# Tamaño de los cuadrados que representan cada fila y columna en el tablero
SQUARESIZE = 100

# Se crea el objeto de la clase ConnectFour
board = CF.ConnectFour(np.zeros((6, 7), dtype=int), 6, 7)

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

# Inicializa todo los modulos de pygame
pygame.init()

# Fuente de texto que se usará en la etiqueta
myfont = pygame.font.SysFont("monospace", 75)

def draw_board(board: CF.ConnectFour) -> None:
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
    
def draw_piece(center: float) -> None:
    """
    Dibuja la ficha del jugador
    """
    
    pygame.draw.circle(screen, RED, center, RADIUS)
    
def draw_top() -> None:
    """
    Dibuja el tope de la ventana de blanco
    """
    pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))

def remove_piece_from_top() -> None:
    """
    Borra la ficha que está en el tope de la ventana
    """
    
    # Dibuja el tope de la ventana de blanco (para borrar la ficha del tope)
    draw_top()
    
    # Se actualiza la ventana para que se refleje los cambios        
    pygame.display.update()
     
def winning_game(player: int) -> None:
    """
    Diseña el mensaje de que jugador gano y finaliza el juego   
    """
    
    # Se elimina la ficha del tope para mostrar el mensaje
    remove_piece_from_top()
    
    # Si es el jugador humano escoge el rojo, si es la AI el amarillo
    color = (DARK_YELLOW, RED)[player == GM.HUMAN_PLAYER]
    
    # Mensaje que será mostrado dependiendo el ganador
    msg = ("The AI beat you", "You have won!!!")[player == GM.HUMAN_PLAYER]
    
    # Se crea la etiqueta con el texto que indica el ganador
    label = myfont.render(msg, 1, color)
                        
    # Dibuja la etiqueta en la posicion dada de la ventana de pygame
    screen.blit(label, (20, 10))
                        
    GM.end_game()
    
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
    GM.end_game()
    