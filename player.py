from board import Direction, Rotation, Action
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError


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

class PlayerConnor(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        """
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
        """
                

            

    def choose_action(self, board):
        #self.print_board(board)
        
        time.sleep(0.5)
        bestMoves = []
        sandbox1 = board.clone()   # 2 sandboxes represent 2 horizontal directions of moving
        sandbox2 = board.clone()
        
        i=0
        for i in range(0,5):
            j=i
            for j in range(i):
                sandbox1.move(Direction.Left)
  
    
        bestMoves.append(Rotation.Clockwise)
        bestMoves.append(Direction.Right)
        bestMoves.append(Direction.Right)
        bestMoves.append(Direction.Right)
            
        bestMoves.append(Direction.Right)
        if board.falling.right == 9:
            return None
        return bestMoves
        
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
