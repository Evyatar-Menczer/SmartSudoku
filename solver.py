
class Solver:

    def __init__(self,size=9):
        self.board = None
        self.size = size

    def valid_row(self,row,to_enter):
        return all([to_enter != self.board[row][j] for j in range(9)])

    def valid_col(self,col,to_enter):
        return all([to_enter != self.board[i][col] for i in range(9)])

    def valid_grid(self,row,col,num):
        grid_col = int(col/3) * 3
        grid_row = int(row/3) * 3
        for i in range(self.size):
            if i%3 == 0 and i != 0:
                grid_row += 1
                grid_col = int(col/3) * 3
            if self.board[grid_row][grid_col] == num:
                return False
            grid_col += 1
        return True


    def valid_placement(self,row,col,num):
        if not self.valid_col(col,num):
            return False
        elif not self.valid_row(row,num):
            return False
        elif not self.valid_grid(row,col,num):
            return False
        return True

    def outer_solve(self,board):
        self.board = board
        def inner_solve(row=0, col=0):
            self.board = board
            row,col = self.next_cell_to_fill(row,col)
            if row == -1:
                return True
            for val in range(1,10):
                if self.valid_placement(row,col,val):
                    self.board[row][col] = val
                    if inner_solve(row, col):
                        return True
                    self.board[row][col] = 0
            return False
        return inner_solve()

    def next_cell_to_fill(self,i , j):
        # for x in range(i, 9):
        #     for y in range(j, 9):
        #         if self.board[x][y] == 0:
        #             return x, y

        for x in range(i, 9):
            for y in range(0, 9):
                if self.board[x][y] == 0:
                    return x, y
        return -1, -1

    def pretty_print(self):
        for j in range(self.size):
            if j%3 == 0 and j != 0:
                print('-'*21)
            for i in range(self.size):
                if i%3 == 0 and i != 0:
                    print('|',end=' ')
                print(self.board[j][i],end=' ')
            print()
