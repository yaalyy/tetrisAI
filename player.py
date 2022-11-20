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
        
        self.aggregateWeight = -2.60    #weights referenced from https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
        self.completeLinesWeight = 0.760666
        self.holesWeight = -6.70
        self.bumpinessWeight = -0.1750
        self.topHeightWeight = 3.60
        
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
            for y in range(0,board.height):   #scannig from top to bottom, from left to right
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
        for i in range(9):
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
        rowTransition = 0
        freeSpace = set()    #represent all coordinates of free space in the container.
        for i in range(0,board.width):
            for j in range(board.height - self.getContainerHeight(board), board.height):
                freeSpace.add((i,j))
        
        freeSpace = freeSpace.difference(board.cells)  #remove all non-free coordinates from the set
        
        for (x,y) in freeSpace:
            if x == 0:
                rowTransition = rowTransition + 1
                if (x+1,y) not in freeSpace:
                    rowTransition = rowTransition + 1
            elif x == board.width - 1:
                rowTransition = rowTransition + 1
                if (x-1,y) not in freeSpace:
                    rowTransition = rowTransition + 1
            else:
                if ((x-1,y) not in freeSpace):
                    rowTransition = rowTransition + 1
                if ((x+1,y) not in freeSpace):
                    rowTransition = rowTransition + 1
                    
        return rowTransition
        
    def getColumnTransition(self,board):
        columnTransition = 0
        xValid = []
        for (x,y) in board.cells:
            if x not in xValid:
                xValid.append(x)
                
        freeSpace = set()  #represent all coordinates of free space in the container.
        for i in range(0,board.width):
            if i in xValid:
                for j in range(0,board.height):
                    freeSpace.add((i,j))
        freeSpace = freeSpace.difference(board.cells)  #remove all non-free coordinates from the set
        for (x,y) in freeSpace:
            if y == board.height - 1:
                columnTransition = columnTransition + 1
                if (x,y-1) not in freeSpace:
                    columnTransition = columnTransition + 1
            elif y == 0:
                columnTransition = columnTransition + 1
                if (x,y+1) not in freeSpace:
                    columnTransition = columnTransition + 1
            else:
                if (x,y+1) not in freeSpace:
                    columnTransition = columnTransition + 1
                if (x,y-1) not in freeSpace:
                    columnTransition = columnTransition + 1
            
            
        return columnTransition
    def getTopHeight(self,board):
        maxHeight = board.height
        for (x,y) in board.cells:
            if y < maxHeight:
                maxHeight = y
        
        
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
        columns = self.generate_column_height(board)
        
        for x in range(board.width):
            for y in range(columns[x], board.height):
                if y == 0:
                    break   # 0 means this column is empty, so skip it
                else:
                    if (x,y) not in board.cells:
                        holes = holes + 1
        return holes
    
    def getWellSums(self,board):
        wellSum = 0
        freeSpace = set()    #represent all coordinates of free space in the container.
        for i in range(0,board.width):
            for j in range(board.height - self.getContainerHeight(board), board.height):
                freeSpace.add((i,j))
        freeSpace = freeSpace.difference(board.cells)   #remove all non-free coordinates from the set
        for (x,y) in freeSpace:
            if x == 0:
                if ((x+1,y) in board.cells):
                    wellSum = wellSum + 1
                    while ((x+1,y-1) in board.cells) and ((y-1) >= (board.height - self.getContainerHeight(board))) and ((x,y-1) not in board.cells):
                        wellSum = wellSum + 1
                        y = y - 1
            if x == board.width - 1:
                if ((x-1,y) in board.cells):
                    wellSum = wellSum + 1
                    while ((x-1,y-1) in board.cells) and ((y-1) >= (board.height - self.getContainerHeight(board))) and ((x,y-1) not in board.cells):
                        wellSum = wellSum + 1
                        y = y - 1
            else:
                if ((x+1,y) in board.cells) and ((x-1,y) in board.cells):
                    wellSum = wellSum + 1
                    while ((x-1,y-1) in board.cells) and ((x+1,y-1) in board.cells) and ((y-1) >= (board.height - self.getContainerHeight(board))) and ((x,y-1) not in board.cells):
                        wellSum = wellSum + 1
                        y = y - 1
        
        return wellSum
    
    def makeSimulation(self,board):
        bestMoves = []
        bestWeight = -99999999
        for i in range(0,board.width):
            
            
            for k in range(0,4):
                sandbox1 = board.clone()  #sandbox1 represents moving left
                currentMoves = []
                currentWeight = -99999999
                landed = False
                leftCoordinate = sandbox1.falling.left
                
                for rotation in range(0,k):
                    if sandbox1.falling is not None:
                        landed = sandbox1.rotate(Rotation.Clockwise)
                        currentMoves.append(Rotation.Clockwise)
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
                #rowsEliminated = self.getRowsEliminated(sandbox1)   #A Drop move has been acted inside this function
                #currentMoves.append(Direction.Drop)
                aggregateHeight = self.getAggregateHeight(sandbox1)
                numberOfHoles = self.getNumberOfHoles(sandbox1)
                bumpiness = self.getBumpiness(sandbox1)
                topHeight = self.getTopHeight(sandbox1)
               
                
                currentWeight = aggregateHeight*self.aggregateWeight + numberOfHoles*self.holesWeight + bumpiness*self.bumpinessWeight + topHeight*self.topHeightWeight
                
                if currentWeight > bestWeight:
                    bestMoves = currentMoves
                    bestWeight = currentWeight
       
        return bestMoves
        
    def choose_action(self, board):
        
        #time.sleep(0.5)
        bestMoves = []
        
        bestMoves = self.makeSimulation(board)
        
        
        if len(bestMoves) > 0:
            
            return bestMoves
        else:
            return None 
        
        
            
SelectedPlayer = PlayerConnor
