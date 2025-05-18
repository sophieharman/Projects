import pygame
from sudoku import Sudoku

def draw_board(screen, sudoku, font):
    size = 540
    block_size = size // 9
    screen.fill((255, 255, 255))

    for i in range(9):
        for j in range(9):
            num = sudoku.grid[i][j]
            if num != 0:
                text = font.render(str(num), True, (0, 0, 0))
                screen.blit(text, (j * block_size + 20, i * block_size + 10))

    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * block_size), (size, i * block_size), thickness)
        pygame.draw.line(screen, (0, 0, 0), (i * block_size, 0), (i * block_size, size), thickness)