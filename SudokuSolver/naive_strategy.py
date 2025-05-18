import numpy as np

class Naive:

    def update_possible_moves(self, row, col, value):
        # Row
        for j in range(9):
            if j != col and value in self.possible_moves[row, j]:
                self.possible_moves[row, j].remove(value)

        # Column
        for i in range(9):
            if i != row and value in self.possible_moves[i, col]:
                self.possible_moves[i, col].remove(value)

        # Square
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                r, c = box_row_start + i, box_col_start + j
                if (r, c) != (row, col) and value in self.possible_moves[r, c]:
                    self.possible_moves[r, c].remove(value)


    def __init__(self, grid):
        # Possible moves for each board entry
        possible_moves = np.empty((9, 9), dtype=object)
        for i in range(9):
            for j in range(9):
                possible_moves[i, j] = list(range(1, 10))
        self.possible_moves = possible_moves

        # Remove invalid values based on the initial board
        for i in range(9):
            for j in range(9):
                value = grid[i, j]
                if value != 0:
                    self.update_possible_moves(i, j, value)

    def make_move(self, board):
        made_move = False
        for _ in range(20):
            for i in range(9):
                for j in range(9):
                    if board[i, j] != 0:
                        self.update_possible_moves(i, j, board[i, j])
                        continue
                    if (board[i, j] == 0 and len(self.possible_moves[i, j]) == 1):
                        value = self.possible_moves[i, j][0]
                        board[i, j] = value
                        self.update_possible_moves(i, j, value)
                        made_move = True  # A move was made
        return made_move  # No move made