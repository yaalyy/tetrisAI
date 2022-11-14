from board import Direction, Rotation, Action
from random import Random
import random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError

"""
class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

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
                

            

    def choose_action(self, board):
        self.print_board(board)
        time.sleep(0.5)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])
""" 

class PlayerConnor(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)
        self.flag = 0
        self.times = 0
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
                    
                
            
            
                

            

    def choose_action(self, board):
        #self.print_board(board)
        
        #time.sleep(0.5)
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
             
        #waiting for sandbox2 to add
        print(board.clean())
        times = self.times
        xList = []
        for (x,y) in board.cells:
            if x not in xList:
                xList.append(x)
        #while(times in xList):
          #  times = random.randint(0,9)
        
        times = times - 5
        if times <= 0:
            for i in range(0,-times):
                bestMoves.append(Direction.Left)
        elif times >= 1:
            for i in range(0,times):
                bestMoves.append(Direction.Right)
                
        bestMoves.append(Direction.Drop)
        
        self.times = self.times+1
        if(self.times > 9):
            self.times = 0
        if len(bestMoves) > 0:
            return bestMoves
        else:
            return None 
        
        """
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])
            
        """
            
SelectedPlayer = PlayerConnor
