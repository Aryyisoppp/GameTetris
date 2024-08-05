import pygame
import random

# Initialize the pygame
pygame.init()

# Set up the display
width, height = 300, 600
block_size = 30
cols, rows = width // block_size, height // block_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# Define the shapes of the single parts
shapes = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 1, 1], [1, 0, 0]],  # J shape
    [[1, 1, 1], [0, 0, 1]]   # L shape
]

colors = [
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 165, 0)
]

# Define the Tetromino class
class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(shapes)
        self.color = colors[shapes.index(self.shape)]
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(cols)] for _ in range(rows)]

    for y in range(rows):
        for x in range(cols):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.image()

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 1:
                positions.append((shape.x + j, shape.y + i))
    return positions

def valid_space(shape, grid):
    accepted_positions = [[(x, y) for x in range(cols) if grid[y][x] == (0, 0, 0)] for y in range(rows)]
    accepted_positions = [x for item in accepted_positions for x in item]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def draw_grid(surface, grid):
    for y in range(rows):
        for x in range(cols):
            pygame.draw.rect(surface, grid[y][x], (x*block_size, y*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 5)

def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
    return increment

def draw_window(surface, grid):
    surface.fill((0, 0, 0))
    draw_grid(surface, grid)
    pygame.display.update()

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Tetromino(5, 0)
    next_piece = Tetromino(5, 0)
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = Tetromino(5, 0)
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(screen, grid)

        if check_lost(locked_positions):
            run = False

    pygame.display.quit()

main()
