# Librerias
import copy

class ConnectFour():
    def __init__(self, board: list, rows: int, columns: int):
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
                newChild = ConnectFour(copy.copy(self.board), self.ROWS, self.COLUMNS) 
                
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