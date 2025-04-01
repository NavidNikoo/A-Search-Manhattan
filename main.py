import pygame
import math
from queue import PriorityQueue
from algorithms import AStar, Node
from visualization import draw, make_grid, get_clicked_position

# Initialize pygame
pygame.init()
pygame.font.init()

# Window settings
WIDTH = 700
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Car")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (160, 160, 160)

# Button dimensions
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

class Button:
    def __init__(self, x, y, text):
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.text = text
        self.color = LIGHT_GRAY
        self.active = False

    def draw(self, win):
        """Draw button on the screen"""
        color = DARK_GRAY if self.active else self.color
        pygame.draw.rect(win, color, self.rect, border_radius=8)
        font = pygame.font.SysFont('arial', 22, bold=True)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main(SCREEN, width):
    mode = None
    ROWS = 25
    grid = make_grid(ROWS, width)

    start = None
    end = None
    running = True
    clock = pygame.time.Clock()  # Limit FPS

    # Adjusted button positions
    button_y = HEIGHT - 80
    buttons = {
        'block': Button(10, button_y, "Block"),
        'open': Button(120, button_y, "Open"),
        'start': Button(230, button_y, "Start"),
        'goal': Button(340, button_y, "Goal"),
        'run': Button(450, button_y, "Run A*"),
        'reset': Button(560, button_y, "Reset")
    }

    while running:
        clock.tick(60)  # Reduce flickering by limiting FPS

        # Only update if needed
        SCREEN.fill(WHITE)

        # Draw grid **before** buttons to prevent overwriting
        draw(SCREEN, grid, ROWS, width)

        # Draw buttons **last** so they appear correctly
        button_rects = []
        for key, button in buttons.items():
            button.active = (mode == key)
            button.draw(SCREEN)
            button_rects.append(button.rect)  # Store button areas for optimized updates

        # Only update button areas instead of the full screen
        pygame.display.update(button_rects)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for key, button in buttons.items():
                    if button.is_clicked(pos):
                        mode = key  # Update mode **only when clicked**

                        if mode == 'run' and start and end:
                            for row in grid:
                                for node in row:
                                    node.update_neighbors(grid)
                            AStar(lambda: draw(SCREEN, grid, ROWS, width), grid, start, end)
                        elif mode == 'reset':
                            start = None
                            end = None
                            grid = make_grid(ROWS, width)

            if pygame.mouse.get_pressed()[0]:  # Left click for grid
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                if row < ROWS and col < ROWS:  # Avoid clicking outside grid
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    elif spot != end and spot != start:
                        spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right click to erase grid
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                if row < ROWS and col < ROWS:
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    AStar(lambda: draw(SCREEN, grid, ROWS, width), grid, start, end)

    pygame.quit()

main(SCREEN, WIDTH)
