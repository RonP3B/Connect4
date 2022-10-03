import math
import sys
from Helpers import BoardManagement as BM
from Helpers import GameManagement as GM

def main():
    BM.draw_board(BM.board)
    
    while not GM.game_over:
        for event in BM.pygame.event.get():
            if event.type == BM.pygame.QUIT:
                sys.exit()
                
            if event.type == BM.pygame.MOUSEMOTION and GM.turn == GM.HUMAN_PLAYER:
                BM.draw_top()
                posX = event.pos[0]
                center = (posX, int(BM.SQUARESIZE / 2))
                BM.draw_piece(center)
                     
            BM.pygame.display.update()

            if event.type == BM.pygame.MOUSEBUTTONDOWN and GM.turn == GM.HUMAN_PLAYER:
                posX = event.pos[0]
                col = int(math.floor(posX / BM.SQUARESIZE))
                
                if BM.board.is_valid_location(col):
                    GM.play_human_ply(BM.board, col)
                    GM.is_goal_state(BM.board, GM.HUMAN_PLAYER)
                    BM.draw_board(BM.board)
                    
        if GM.turn == GM.AI_PLAYER and not GM.game_over:
            BM.remove_piece_from_top()
            GM.play_AI_ply(BM.board, 3)
            GM.is_goal_state(BM.board, GM.AI_PLAYER)
            BM.draw_board(BM.board)
             
        if GM.game_over: 
            BM.pygame.time.wait(7000)
                                       
if __name__ == '__main__': main()