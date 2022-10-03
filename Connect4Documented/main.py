# Librerias
import math
import sys

# Paquetes
from Helpers import BoardManagement as BM
from Helpers import GameManagement as GM

def main():
    # Dibuja el diseño del tablero en la ventana de pygame
    BM.draw_board(BM.board)
    
    #Bucle que correrá siempre y cuando el juego no se haya terminado,
    #la variable 'game_over' es booleana, como hay una negación (el not)
    #se entrará en el bucle cuando 'game_over' sea falso
    while not GM.game_over:
        
        # Bucle que sirve para capturar todos los eventos que suceden en la
        # ventana de pygame
        for event in BM.pygame.event.get():
            
            #Si se presiona el botón de cerrar de la ventana de pygame
            if event.type == BM.pygame.QUIT:
                #Cierra la ventana y acaba la ejecución del programa
                sys.exit()

            # Si se mueve el mouse en la ventana de pygame en el turno del jugador
            if event.type == BM.pygame.MOUSEMOTION and GM.turn == GM.HUMAN_PLAYER:
                # Dibuja el tope de la ventana de blanco
                BM.draw_top()
                
                # Obtiene la posicion en x-axis en la que se mueve el mouse
                posX = event.pos[0]
                
                # Posición central del circulo
                center = (posX, int(BM.SQUARESIZE / 2))

                # Dibuja la ficha del jugador
                BM.draw_piece(center)
            
            # Se actualiza la ventana para que se reflejen los cambios        
            BM.pygame.display.update()

            # Si se clickea en la ventana de pygame en el turno del jugador
            if event.type == BM.pygame.MOUSEBUTTONDOWN and GM.turn == GM.HUMAN_PLAYER:
                
                # Posicion en el x-axis(como la x del plano cartesiano) donde se clickeó
                # o sea, la parte horizontal de la ventana donde el usuario dió click
                posX = event.pos[0]
                    
                # Se divide 'posX' entre el tamaño del cuadrado, esto para determinar que 
                # columna representa en la matriz la parte donde el usuario clickeó
                col = int(math.floor(posX / BM.SQUARESIZE))
                
                # Si la columna elegida no está llena realiza la jugada
                if BM.board.is_valid_location(col):
                    
                    # Se realiza la jugada del humano
                    GM.play_human_ply(BM.board, col)
                    
                    # Se verifica si el humano ganó el juego o quedo si quedó empate
                    GM.is_goal_state(BM.board, GM.HUMAN_PLAYER)
                        
                    # Se vuelve a dibujar el tablero para que se reflejen los cambios
                    BM.draw_board(BM.board)

        # Turno de la IA
        if GM.turn == GM.AI_PLAYER and not GM.game_over:
            # Se borra la ficha del jugador humano
            BM.remove_piece_from_top()
            
            # Se juega el turno de la AI con un limite de 2 segundos
            GM.play_AI_ply(BM.board, 3)
        
            # Se verifica si la AI ganó el juego o si quedó empate
            GM.is_goal_state(BM.board, GM.AI_PLAYER)
            
            # Se vuelve a dibujar el tablero para que se reflejen los cambios
            BM.draw_board(BM.board)
             
        # Sí el juego ha finalizado
        if GM.game_over: 
            
            # Se hace una pausa de 7 segundos para que se pueda apreciar el resultado
            # y luego ya acaba la ejecución
            BM.pygame.time.wait(7000)
                                       
if __name__ == '__main__':
    main()