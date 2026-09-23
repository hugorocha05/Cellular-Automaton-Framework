"""
This code implements a simple cellular automaton framework capable of simulating Conway's Game of Life and other birth/survival rule sets using only vanilla Python for the game logic and Pygame for the visualization.
The idea is to understand how these Automata work and to serve as a base for later projects like attempting to find alternative rules that still lead to interesting simulations.
This implementation also considers a Toroidal (Torus-like) world/plane, where boundaries behave with "wrap-around" behaviour.
"""

import pygame
import random

# Pygame Setup ------------------------------------------------------

pygame.init()

screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Cellular Automaton Framework")

clock = pygame.time.Clock()

# -------------------------------------------------------------------


# Functions ---------------------------------------------------------

def create_random_matrix(rows, cols, live_rate=0.10):
    matrix = []

    for _ in range(rows):
        row = []
        for _ in range(cols):
            pick = random.random()

            if pick < live_rate:
                row.append(1)
            else:
                row.append(0)

        matrix.append(row)

    return matrix

def create_null_matrix(rows, cols):
    matrix = []

    for _ in range(rows):
        matrix.append([0] * cols)

    return matrix

def show_grid(matrix, border=True):
    # Calculate resolution based on screen and matrix size, so each cell can have the correct width and length to fill the screen while staying consistent with the matrix 
    # Ex: 700x700 screen sith a 10x10 matrix would yield cells of size 70x70

    res_x = screen_width // len(matrix[0])
    res_y = screen_height // len(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            x = j * res_x  # Find the correct coordinates based on the resolution
            y = i * res_y

            rect_obj = (x, y, res_x, res_y)

            if matrix[i][j] == 1:
                pygame.draw.rect(screen, (255, 255, 255), rect_obj)  # Draw live cell

            if border:
                pygame.draw.rect(screen, (50, 50, 50), rect_obj, width=1)  # Draw border to get grid pattern

def apply_rules(cell_state, num_live_neighbors, birth_conditions, survival_conditions):
    if cell_state == 0 and num_live_neighbors in birth_conditions:  # Birth
        return 1
    
    elif cell_state == 1 and num_live_neighbors in survival_conditions: # Survival
        return 1

    else:
        return 0

def update_grid(matrix, neighbors, birth_conditions, survival_conditions):
    new_matrix = []

    for i in range(len(matrix)):
        new_row = []

        for j in range(len(matrix[i])):

            num_live_neighbors = 0

            for neighbor in neighbors:
                # Determine the neighbor's coordinate under toroidal boundary conditions (mathematically calculate the "wrap-around" positions)
                neighbor_i = (i + neighbor[0]) % len(matrix)
                neighbor_j = (j + neighbor[1]) % len(matrix[i])

                # Count live neighbors
                if matrix[neighbor_i][neighbor_j] == 1:
                    num_live_neighbors += 1

            new_state = apply_rules(matrix[i][j], num_live_neighbors, birth_conditions, survival_conditions)

            new_row.append(new_state)

        new_matrix.append(new_row)

    return new_matrix
    

def run_sim(rows, cols, neighbors, birth_conditions, survival_conditions, border=True):
    matrix = create_null_matrix(rows, cols)  # Start with a grid of all dead cells

    running = True
    paused = True
    step = False

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pausing
                    paused = not paused

                if paused:
                    if event.key == pygame.K_RIGHT:  # Step
                        step = True

                    elif event.key == pygame.K_r:  # Randomize
                        matrix = create_random_matrix(rows, cols)

                    elif event.key == pygame.K_c:  # Clear
                        matrix = create_null_matrix(rows, cols)

            elif event.type == pygame.MOUSEBUTTONDOWN and paused:
                if event.button == 1:  # Left Click
                    x, y = event.pos

                    # Do the opposite operations of showing the grid. Instead of having a matrix and finding the correct coordinates to draw the cell, I want to know what value of the matrix a drawn cell corresponds to
                    res_x = screen_width // len(matrix[0])
                    res_y = screen_height // len(matrix)

                    j = x // res_x
                    i = y // res_y

                    matrix[i][j] = 1 - matrix[i][j]  # Invert the cell state

        if not paused or (paused and step):
            matrix = update_grid(matrix, neighbors, birth_conditions, survival_conditions)  # Only update states if playing or stepping through
            step = False

        if paused:
            screen.fill((60, 60, 60))  # Lighter gray
        else:
            screen.fill((40, 40, 40))  # Dark gray

        show_grid(matrix, border)

        pygame.display.flip()

        clock.tick(8)

    pygame.quit()

# -------------------------------------------------------------------


# Run --------------------------------------------------

"""
===== CONTROLS ====
p -> pause/play (the background will appear a lighter grey)
    while paused:
        right-arrow -> step/advance one generation
        r -> randomize grid
        c -> clear grid
        left-click -> change the cell where the mouse is to the opposite state it's currently in

The simulation starts of paused to give the user a chance to edit the grid/cells before running
"""

neighbors = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
]

birth_conditions = [3]
survival_conditions = [2, 3]


run_sim(rows=70, cols=70, neighbors=neighbors, birth_conditions=birth_conditions, survival_conditions=survival_conditions, border=True)

# -------------------------------------------------------------------