import random
import numpy as np
from collections import defaultdict

class Sudoku:

    def __init__(self, difficulty_level="easy"):
        self.grid = np.zeros((9, 9), dtype=int)
        self.difficulty_level = difficulty_level

        # Map each position to its appropriate "square" in the grid
        self.pos_to_square = {}
        for i in range(9):      
            for j in range(9):   
                row, col = i // 3, j // 3
                square_number = row * 3 + col + 1
                self.pos_to_square[(i, j)] = square_number

        # Reverse the square mapping
        self.square_to_pos = defaultdict(list)
        for pos, square in self.pos_to_square.items():
            self.square_to_pos[square].append(pos)

    def initialize_board(self):
        # Repeat until we generate a board with a unique solution
        while True:
            self.grid = np.zeros((9, 9), dtype=int)
            self.fill_board()
            full_solution = self.grid.copy()

            if self.difficulty_level == "easy":
                keepSquares = 36
            elif self.difficulty_level == "medium":
                keepSquares = 32
            elif self.difficulty_level == "hard":
                keepSquares = 28
            else:
                keepSquares = 22

            # Try removing cells while checking uniqueness
            puzzle = full_solution.copy()
            cells = [(r, c) for r in range(9) for c in range(9)]
            random.shuffle(cells)
            removed = 0

            while removed < (81 - keepSquares) and cells:
                r, c = cells.pop()
                backup = puzzle[r, c]
                puzzle[r, c] = 0

                if self.count_solutions(puzzle.copy(), 0, 2) != 1:
                    puzzle[r, c] = backup  # Restore if not unique
                else:
                    removed += 1

            if self.count_solutions(puzzle.copy(), 0, 2) == 1:
                self.grid = puzzle
                break

    def fill_board(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self.valid_move(i, j, num):
                            self.grid[i][j] = num
                            if self.fill_board():
                                return True
                            self.grid[i][j] = 0  # backtrack
                    return False  # no valid number found
        return True  # board completely filled

    def count_solutions(self, board, count=0, limit=2):
        if count >= limit:
            return count
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.valid_move_board(board, i, j, num):
                            board[i][j] = num
                            count = self.count_solutions(board, count, limit)
                            board[i][j] = 0
                            if count >= limit:
                                return count
                    return count
        return count + 1

    def valid_move(self, row, col, value):
        return (self.checkRow(row, value) and 
                self.checkCol(col, value) and 
                self.checkSquare(row, col, value))

    def valid_move_board(self, board, row, col, value):
        for i in range(9):
            if board[row][i] == value or board[i][col] == value:
                return False
        square_num = self.pos_to_square[(row, col)]
        for r, c in self.square_to_pos[square_num]:
            if board[r][c] == value:
                return False
        return True

    def checkRow(self, row, value):
        return value not in self.grid[row]

    def checkCol(self, col, value):
        return value not in self.grid[:, col]

    def checkSquare(self, row, col, value):
        square_num = self.pos_to_square[(row, col)]
        for r, c in self.square_to_pos[square_num]:
            if self.grid[r][c] == value:
                return False
        return True
