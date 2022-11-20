from board import Direction, Rotation, Action
from random import Random
import random
import time
from exceptions import NoBlockException


class Player:
    def choose_action(self, board):
        raise NotImplementedError



class PlayerConnor(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)
        self.flag = 0
        
        self.landingHeightWeight = -4.500158825082766    # weights referenced from EI-Tetris
        self.rowsEliminatedWeight = 3.4181268101392694
        self.rowTransitionWeight = -3.2178882868487753
        self.columnTransitionWeight = -9.348695305445199
        self.numberOfHolesWeight = -7.899265427351652
        self.wellSumsWeight = -3.3855972247263626
        
        self.aggregateWeight = -2.6   #-2.6    #weights referenced from https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
        self.holesWeight = -6.7   #-6.7
        self.bumpinessWeight = -0.1750   #-0.1750
        self.topHeightWeight = 3.6   #3.6
        
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
    
                    
    
    def generate_column_height(self, board):
        
        columns = [0] * board.width

        for x in range(0,board.width):
            for y in range(0,board.height-1):   #scannig from top to bottom, from left to right
                if (x,y) in board.cells:
                    columns[x] = y 
                    break    # when it touches the top of this column, go to check the next column
        return columns
    def getAggregateHeight(self,board):
        
        aggregateHeight = 0
        for x in range(board.width):
            height = 0
            for y in range(board.height):
                if (x,y) in board.cells:
                    height = board.height - y
                    break
            aggregateHeight = aggregateHeight + height
        return aggregateHeight
    
    def getBumpiness(self,board):
        
        total = 0
        columns = self.generate_column_height(board)
        for i in range(board.width - 1):
            total += abs(columns[i] - columns[i+1])
        return total
        
    def getContainerHeight(self,board):     # Container is a collection of all blocks landed
        maxHeight = board.height
        for (x,y) in board.cells:
            if y < maxHeight:
                maxHeight = y
        
        maxHeight = board.height - maxHeight
        return maxHeight    #the total height of container
    
    def getLandingHeight(self,board):
        landingHeight = 0
        blockHeight = board.falling.bottom - board.falling.top + 1
        maxheight = board.height
        
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
        prevHeight = board.height
        for (x,y) in board.cells:
            if y < prevHeight:
                prevHeight = y    
        prevHeight = board.height - prevHeight
        currentHeight = board.height
        board.move(Direction.Drop)
        for (x,y) in board.cells:
            if y < currentHeight:
                currentHeight = y
        currentHeight = board.height - currentHeight
        rowsEliminated = prevHeight - currentHeight
        if rowsEliminated < 0:
            rowsEliminated = 0
        return rowsEliminated   
    
    def getRowTransition(self,board):
        row_trans = 0
        for y in range(board.height - 1, 0, -1):
            for x in range(board.width):
                if ((x,y) in board.cells) and ((x+1,y) not in board.cells):
                    row_trans = row_trans + 1
                if ((x,y) not in board.cells) and ((x+1,y) in board.cells):
                    row_trans = row_trans + 1
        return row_trans 
        
    def getColumnTransition(self,board):
        col_trans = 0
        for x in range(board.width):
            for y in range(board.height - 1, 1, -1):
                if ((x,y) in board.cells) and ((x,y-1) not in board.cells):
                    col_trans = col_trans + 1
                if ((x,y) not in board.cells) and ((x,y-1) in board.cells):
                    col_trans = col_trans + 1
        return col_trans
    
    def getTopHeight(self,board):
        
        maxHeight = board.height - 1
        for (x,y) in board.cells:
            if y < maxHeight:
                maxHeight = y
                
        maxHeight = board.height - 1 - maxHeight
        
        
        return maxHeight    #the top y-coordinate of container
       
    def isHole(self,x,y, board, boardTop):
        
        if y <= boardTop:
            return False
        elif y == boardTop + 1:
            if (x,y-1) in board.cells:
                return True
            else:
                return False
        elif y > boardTop + 1:
            if (x,y-1) in board.cells:
                return True
            else:
                return self.isHole(x,y-1,board,boardTop)
        
    def getNumberOfHoles(self,board):
        
        holes = 0
        for x in range(10):
            holes_in_col = None
            for y in range(24):
                if (holes_in_col == None) and ((x, y) in board.cells):
                    holes_in_col = 0
                if (holes_in_col != None) and ((x, y) not in board.cells):
                    holes_in_col += 1
                
            if holes_in_col is not None:
                holes += holes_in_col
        return holes
    

       
    def getWellSums(self,board):
        wells = 0
        total = 0
        for x in range(board.width):
            for y in range(board.height):
                if (x, y) not in board.cells:
                    
                    if ((x - 1) < 0) or ((x - 1, y) in board.cells):
                        if ((x + 1) > 9) or ((x + 1, y) in board.cells):
                            wells = wells + 1
                    else:
                        i = 0
                        while i<= wells:
                            total += i
                            i += 1
                        wells = 0
        return total
    def makeSimulation(self,board):
        
        bestMoves = []
        bestWeight = -9999999
        for i in range(board.width):
            
            
            for k in range(4):
                sandbox1 = board.clone()  #sandbox1 represents moving left
                currentMoves = []
                currentWeight = -9999999
                landed = False
                leftCoordinate = sandbox1.falling.left
                
                for rotation in range(k):
                    if sandbox1.falling is not None:
                        landed = sandbox1.rotate(Rotation.Anticlockwise)
                        currentMoves.append(Rotation.Anticlockwise)
                        if landed:
                            break
                        else:
                            leftCoordinate = sandbox1.falling.left
                        
                while (leftCoordinate > i) and (landed == False):
                    landed = sandbox1.move(Direction.Left)
                    currentMoves.append(Direction.Left)
                    if sandbox1.falling is not None:
                        leftCoordinate = sandbox1.falling.left
                        
                while (leftCoordinate < i) and (landed == False):
                    landed = sandbox1.move(Direction.Right)
                    currentMoves.append(Direction.Right)
                    if sandbox1.falling is not None:
                        leftCoordinate = sandbox1.falling.left
                if landed == False:
                    sandbox1.move(Direction.Drop)
                    currentMoves.append(Direction.Drop)

        
                currentWeight = self.calScore(sandbox1)
                if currentWeight > bestWeight:
                    bestMoves = currentMoves
                    bestWeight = currentWeight
                #print(bumpiness)
        #time.sleep(2)
        return bestMoves
    
    def calScore(self, board):
        global score_before
        lines_removed = 0
        row_trans = 0
        col_trans = 0
        holes = 0
        total = 0
        height = 0

        score_difference = board.score - score_before

        if 0 <= score_difference < 100:
            lines_removed = 0
        elif 100 <= score_difference < 400:
            lines_removed = 1
        elif 400 <= score_difference < 800:
            lines_removed = 2
        elif 800 <= score_difference < 1600:
            lines_removed = 3
        else:
            lines_removed = 4
        
        row_trans = self.getRowTransition(board)
        col_trans = self.getColumnTransition(board)
        holes = self.getNumberOfHoles(board)
        total = self.getWellSums(board)
        height = self.getTopHeight(board)
        
        score = 34 * lines_removed - 16 * row_trans - 46.5 * col_trans - 39.5 * holes - 17 * total - 22.5 * height

        return score
    def choose_action(self, board):
        global score_before
        score_before = board.score
        #time.sleep(0.5)
        bestMoves = []
        
        bestMoves = self.makeSimulation(board)
        
        
        if len(bestMoves) > 0:
            
            return bestMoves
        else:
            return None 
        
        
            
SelectedPlayer = PlayerConnor
