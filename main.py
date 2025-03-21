import pygame
import math
from queue import PriorityQueue
from algorithms import AStar, Node
from visualization import draw, make_grid, get_clicked_position

#pygame window
WIDTH = 800
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Car")
#window = Window(SCREEN)

#pygame colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
TURQUOISE = (48, 213, 200)


class Button:
    def __init__(self, x, y, width, height, color, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        SCREEN.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def main(SCREEN, width):
    ROWS = 25
    grid = make_grid(ROWS, width)

    start = None
    end = None

    running = True

    while running:
        draw(SCREEN, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]: #Left click, these will just be changed to buttons later
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()


            elif pygame.mouse.get_pressed()[2]: #right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end: #start for algorithm
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                        AStar(lambda: draw(SCREEN, grid, ROWS, width), grid, start, end) #lambda is so we can pass the draw function to the algorithm

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()


main(SCREEN, WIDTH)