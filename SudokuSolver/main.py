import time
from sudoku import Sudoku
from display import draw_board
from naive_strategy import Naive
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((540, 580))
    pygame.display.set_caption("Sudoku")
    font = pygame.font.SysFont("consolas", 30)
    sudoku = Sudoku(difficulty_level="easy")
    sudoku.initialize_board()
    draw_board(screen, sudoku, font)

    naive_solver = Naive(sudoku.grid)

    clock = pygame.time.Clock()
    solving = True

    def is_board_filled(grid):
        # Check if every cell in the grid is filled
        for row in grid:
            if any(cell == 0 for cell in row):  # 0 signifies empty
                return False
        return True

    start_time = None
    while True:
        screen.fill((255, 255, 255))
        draw_board(screen, sudoku, font)

        if is_board_filled(sudoku.grid):
            if solving:  
                solving = False
                solving_time = time.time() - start_time - 1 # Accounting for pytime game delay
            message = f"Solved in {solving_time:.3f} seconds!"
            text = font.render(message, True, (0, 128, 0))
        elif solving:
            text = font.render("Solving...", True, (0, 0, 0))
        else:
            text = font.render("Failed to solve!", True, (255, 0, 0))  # Red text for failure

        screen.blit(text, (10, 545))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if solving:
            if start_time is None:
                start_time = time.time()
            pygame.time.delay(1000)
            move_made = naive_solver.make_move(sudoku.grid)
            if not move_made:
                solving = False

        clock.tick(60)


if __name__ == "__main__":
    main()