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
    def to_matrix(self,board):
        matrix = [[None] * board.width for i in range(board.height)]
        for (x,y) in board.cells:
          #  print(x,y)
            matrix[y][x] = 1
        return matrix
    def Get_landing_Height(self,board):
        max_height = board.height + 1
        for cell in board.cells:
            if (cell[1] < max_height):
                max_height = cell[1]
        return max_height
    def Get_eroded_Piece_cells_metirc(self,board):
        lines = 0
        usefulblock = 1

        matrix = self.to_matrix(board)
        flag = True
        # 按行遍历 找有方块的行数 如果有一行全不为空 lines ++ 为2 usefulblock++
        for i in range(len(matrix) - 1, 0, -1):  # 行
            count = 0
            for j in range(len(matrix[0])):  # 列
                if matrix[i][j] is not None:
                    count += 1
            if count == len(matrix[0]):  # 有一行全满
                lines += 1
                for k in range(len(matrix[0])):
                    if matrix[i][k] == 2:  # 如果有该方块
                        usefulblock += 1
            # 整行未填充，则跳出循环
            if count == 0:
                break
        # graph = self.to_graph(matrix)
        return lines * usefulblock
    def Get_Row_trans(self,board):
        transition = 0
        matrix = self.to_matrix(board)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])-1):
                if matrix[i][j] == None and matrix[i][j + 1] != None:
                    transition += 1
                if matrix[i][j] != None and matrix[i][j + 1] == None:
                    transition += 1
        return transition
    
    def Get_Col_trans(self,board):
        transition = 0
        matrix = self.to_matrix(board)
        for j in range(len(matrix[0])):
            for i in  range(len(matrix)-1):
                if matrix[i][j] == None and matrix[i+1][j] !=None:
                    transition += 1
                if matrix[i][j] !=None and matrix[i+1][j] == None:
                    transition+=1
        return transition
    
    def Get_Buried_holes(self,board):
         holes = 0
         matrix = self.to_matrix(board)
         for j in range(len(matrix[0])):  # 列
             flag = 0
             colHoles = 0
             for i in range(len(matrix)):  # 行
                 if flag == 0 and matrix[i][j] != None:
                     flag = 1
                 if flag ==1  and matrix[i][j] == None:
                      colHoles += 1
             holes += colHoles
         return holes
     
    def Get_board_wells(self,board):
        sum_n = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153, 171, 190, 210, 231, 253, 276,
                 300]  # 根据井深计算的分数数组
        wells = 0
        sum = 0

        matrix = self.to_matrix(board)
      #  for i in matrix:
       #     print(i)
        for j in range(len(matrix[0])):  # 列
            for i in range(len(matrix) - 1, 0, -1):  # 行
                if matrix[i][j] == None:
                    if (j - 1 < 0 or matrix[i][j - 1] != None) and (j + 1 >= board.width or matrix[i][j + 1] != None):
                        wells += 1
                    else:
                        sum += sum_n[wells]
                        wells = 0
        if (wells != 0):
            sum += sum_n[wells]
        return sum
    
    def score_board(self,cloneboard):
        lh = self.Get_landing_Height(cloneboard)
        epcm = self.Get_eroded_Piece_cells_metirc(cloneboard)
        rt = self.Get_Row_trans(cloneboard)
        ct = self.Get_Col_trans(cloneboard)
        bh = self.Get_Buried_holes(cloneboard)
        bw = self.Get_board_wells(cloneboard)
        return -45 * lh + 34 * epcm - 32 * rt - 93 * ct - 79 * bh - 34 * bw+150*min([y for x,y in cloneboard.cells])+150*sum([y for x,y in cloneboard.cells])/len(cloneboard.cells)
    
    def try_move(self,board,xtarget,rtarget):
        cloneboard  = board.clone()
        times_rotate = 0
        move_ans=[]
        res = False
        trymove = None
        while True:
            if times_rotate < rtarget :
                trymove = Rotation.Anticlockwise
                times_rotate+= 1
            elif cloneboard.falling.left < xtarget:
                trymove = Direction.Right        # trymove = [Direction.Right for i in range(xtarget-cloneboard.falling.left)]
            elif cloneboard.falling.left >xtarget:
                trymove = Direction.Left         #  trymove = [Direction.Left for i in range(cloneboard.falling.left-xtarget)]
            else:
                trymove = Direction.Drop

            if isinstance(trymove, Direction):
                res = cloneboard.move(trymove)
            elif isinstance(trymove,Rotation):
                res = cloneboard.rotate(trymove)
            move_ans.append(trymove)

            if res:
                #这时会把cell放到board里面
                score = self.score_board(cloneboard)
                return score,move_ans
    def choose_action(self, board):
        best_score = 0
        bestmove = None
        for xtarget in range(10):
            for rtarget in range(4):
                score ,move = self.try_move(board,xtarget,rtarget)
                if score > best_score:
                    best_score = score
                    bestmove =  move
      #  print( "ans", bestmove)
        return bestmove       
SelectedPlayer = PlayerConnor
