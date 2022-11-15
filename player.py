from board import Direction, Rotation, Action
from random import Random
import random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError



class PlayerConnor(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)
        self.flag = 0
        
    def print_board(self, board):
        
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
    
    def getLandingHeight(self,board):
        landingHeight = 0
        blockHeight = board.falling.bottom - board.falling.top + 1
        maxheight = 24
        xList = []
        for (x,y) in board.falling.cells:
            if x not in xList:
                xList.append(x)
        
        for (x,y) in board.cells:
            if x in xList:
                if y < maxheight:
                    maxheight = y
        
        maxheight = board.height - maxheight
        
        landingHeight = maxheight + (blockHeight/2)
        
        return landingHeight
                    
    def getRowsEliminated(self,board):
        prevHeight = 24
        for (x,y) in board.cells:
            if y < prevHeight:
                prevHeight = y    
        prevHeight = board.height - prevHeight
        currentHeight = 24
        board.move(Direction.Drop)  
        for (x,y) in board.cells:
            if y < currentHeight:
                currentHeight = y
        currentHeight = board.height - currentHeight
        rowsEliminated = prevHeight - currentHeight
        return rowsEliminated   
    
    
            
    def choose_action(self, board):
        #self.print_board(board)
        
        time.sleep(0.5)
        bestMoves = []
        bestWeight = 0
        sandbox1 = board.clone()   # 2 sandboxes represent 2 horizontal directions of moving
        sandbox2 = board.clone()
        
    
        for i in range(0,6):
            j=i
            currentMoves = []
            currentWeight = 0
            
            for k in range(0,4):
                sandbox1 = board.clone()
                if k == 1:
                    sandbox1.rotate(Rotation.Clockwise)
                    currentMoves.append(Rotation.Clockwise)
                elif k == 2:
                    sandbox1.rotate(Rotation.Clockwise)
                    sandbox1.rotate(Rotation.Clockwise)
                    currentMoves.append(Rotation.Clockwise)
                    currentMoves.append(Rotation.Clockwise)
                elif k == 3:
                    sandbox1.rotate(Rotation.Anticlockwise)
                    currentMoves.append(Rotation.Anticlockwise)
                    
                for j in range(i):
                    sandbox1.move(Direction.Left)
                    currentMoves.append(Direction.Left)
                currentMoves.append(Direction.Drop)
                print(self.getLandingHeight(sandbox1))
                sandbox1.move(Direction.Drop)
                self.print_board(sandbox1)
                
                
             
        #waiting for sandbox2 to add
       
        
        if len(bestMoves) > 0:
            return bestMoves
        else:
            return None 
        
        
            
SelectedPlayer = PlayerConnor
