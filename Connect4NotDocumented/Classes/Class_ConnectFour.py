import copy

class ConnectFour():
    def __init__(self, board: list, rows: int, columns: int):
        self.ROWS = rows
        self.COLUMNS = columns
        self.board = board
        
    def is_valid_location(self, col: int) -> bool:
        return self.board[0][col] == 0
    
    def get_next_open_row(self,col:int) -> int:
        for r in range(self.ROWS -1, -1, -1): 
            if self.board[r][col] == 0: return r
    
    def drop_piece(self, row: int, col: int, piece: int) -> None:       
        self.board[row][col] = piece
            
    def check_all_horizontals(self, four_connected: list) -> bool:
        for r in range(self.ROWS): 
            for c in range(self.COLUMNS - 3):              
                if (self.board[r][c:c + 4] == four_connected).all(): return True
                
        return False
    
    def check_all_verticals(self, four_connected:list) -> bool:
        for c in range(self.COLUMNS):
            for r in range(self.ROWS - 3):
                if (self.board[r:r+4,c] == four_connected).all(): return True

        return False
    
    def check_all_diagonals(self, four_connected:list) -> bool:     
        for c in range(self.COLUMNS - 3):
            for r in range(self.ROWS - 3):       
                if ([self.board[r+x][c+x] for x in range(4)] == four_connected): return True

        return False
    
    def check_all_negative_diagonals(self, four_connected:list) -> bool:
        for c in range(self.COLUMNS - 3):
            for r in range(3, self.ROWS):
                if [self.board[r-x][c+x] for x in range(4)] == four_connected: return True
        
        return False
    
    def expand(self, player: int) -> list:
        children = []

        for col in range(self.COLUMNS):
            if self.is_valid_location(col):
                nextOpenRow = self.get_next_open_row(col)
                newChild = ConnectFour(copy.copy(self.board), self.ROWS, self.COLUMNS) 
                newChild.drop_piece(nextOpenRow, col, player)
                children.append(newChild)
                
        return children
                
    
    def test_win(self, piece: int) -> bool:
        four_connected = [piece for i in range(4)]

        if self.check_all_horizontals(four_connected): return True
        if self.check_all_verticals(four_connected): return True
        if self.check_all_diagonals(four_connected): return True
        if self.check_all_negative_diagonals(four_connected): return True
        
        return False
    
    def test_tie(self) -> bool:        
        for col in range(self.COLUMNS):
            if self.is_valid_location(col):
                return False
            
        return True