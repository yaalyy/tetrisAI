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
        
        self.landingHeightWeight = -4.500158825082766    # weights referenced from EI-Tetris
        self.rowsEliminatedWeight = 3.4181268101392694
        self.rowTransitionWeight = -3.2178882868487753
        self.columnTransitionWeight = -9.348695305445199
        self.numberOfHolesWeight = -7.899265427351652
        self.wellSumsWeight = -3.3855972247263626
        
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
        freeSpace = set()    #represent all coordinates of free space in the container.
        for i in range(0,board.width):
            for j in range(board.height - self.getContainerHeight(board), board.height):
                freeSpace.add((i,j))
        freeSpace = freeSpace.difference(board.cells)   #remove all non-free coordinates from the set
        for (x,y) in freeSpace:
            if self.isHole(x , y, board, board.height-self.getContainerHeight(board)):
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
    
    def makeSimulation(self,board,bestMoves,bestWeight):
        for i in range(0,6):
            
            
            for k in range(0,4):
                sandbox1 = board.clone()  #sandbox1 represents moving left
                currentMoves = []
                currentWeight = 0
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
                
                landingHeight = self.getLandingHeight(sandbox1)
                rowsEliminated = self.getRowsEliminated(sandbox1)   #A Drop move has been acted inside this function
                currentMoves.append(Direction.Drop)
                rowTransition = self.getRowTransition(sandbox1)
                columnTransition = self.getColumnTransition(sandbox1)
                numberOfHoles = self.getNumberOfHoles(sandbox1)
                wellSums = self.getWellSums(sandbox1)
                
                currentWeight = landingHeight*self.landingHeightWeight + rowsEliminated*self.rowsEliminatedWeight + rowTransition*self.rowTransitionWeight + columnTransition*self.columnTransitionWeight + numberOfHoles*self.numberOfHolesWeight + wellSums*self.wellSumsWeight
                if currentWeight > bestWeight:
                    bestMoves = currentMoves
                    bestWeight = currentWeight
                
                #print("current weight below:",currentWeight)
                #print("best weight:",bestWeight)
                #self.print_board(sandbox1)
                #time.sleep(3)
        for i in range(6,10):
            
            
            for k in range(0,4):
                sandbox2 = board.clone()  #sandbox2 represents moving right
                currentMoves = []
                currentWeight = 0
                if k == 1:
                    sandbox2.rotate(Rotation.Clockwise)
                    currentMoves.append(Rotation.Clockwise)
                elif k == 2:
                    sandbox2.rotate(Rotation.Clockwise)
                    sandbox2.rotate(Rotation.Clockwise)
                    currentMoves.append(Rotation.Clockwise)
                    currentMoves.append(Rotation.Clockwise)
                elif k == 3:
                    sandbox2.rotate(Rotation.Anticlockwise)
                    currentMoves.append(Rotation.Anticlockwise)
                
                for j in range(i-5):
                    sandbox2.move(Direction.Right)
                    currentMoves.append(Direction.Right)
                
                landingHeight = self.getLandingHeight(sandbox2)
                rowsEliminated = self.getRowsEliminated(sandbox2)   #A Drop move has been acted inside this function
                currentMoves.append(Direction.Drop)
                rowTransition = self.getRowTransition(sandbox2)
                columnTransition = self.getColumnTransition(sandbox2)
                numberOfHoles = self.getNumberOfHoles(sandbox2)
                wellSums = self.getWellSums(sandbox2)
                
                currentWeight = landingHeight*self.landingHeightWeight + rowsEliminated*self.rowsEliminatedWeight + rowTransition*self.rowTransitionWeight + columnTransition*self.columnTransitionWeight + numberOfHoles*self.numberOfHolesWeight + wellSums*self.wellSumsWeight
                if currentWeight > bestWeight:
                    bestMoves = currentMoves
                    bestWeight = currentWeight
                
                #print("current weight below:",currentWeight)
                #print("best weight:",bestWeight)
                #self.print_board(sandbox2)
                #time.sleep(3)
        return bestMoves,bestWeight
        
    def choose_action(self, board):
        
        #time.sleep(0.5)
        bestMoves = []
        bestWeight = -999999999
        
        bestMoves,bestWeight = self.makeSimulation(board,bestMoves,bestWeight)
        
        
        
        
            
            
        
        
        
        if len(bestMoves) > 0:
            
            return bestMoves
        else:
            return None 
        
        
            
SelectedPlayer = PlayerConnor
