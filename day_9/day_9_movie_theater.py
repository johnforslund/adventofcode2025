
############################
##  Day 9: Movie Theater  ##
############################
# https://adventofcode.com/2025/day/9


##############
##  Part 1  ##
##############

# Imports
import numpy as np
import pandas as pd
import os

# Initializing variables
folder_path = "day_9"
file_name = "input.txt"
sample_file_name = "input_sample.txt"

with open(os.path.join(folder_path, sample_file_name), "r") as f:
    original_document = f.read()

# Splitting document into lines
original_document = original_document.split("\n")
# Splitting into list of tuples of ints
original_document = [tuple(int(x) for x in line.split(",")) for line in original_document]
# Converting to numpy array for easier manipulation
red_tiles_coords = np.array(original_document)

print(f"Number of red tile coordinates: {red_tiles_coords.shape[0]}")
print(f"Min & max X coordinate of red tile: {red_tiles_coords[:,0].min()} - {red_tiles_coords[:,0].max()}")
print(f"Min & max Y coordinate of red tile: {red_tiles_coords[:,1].min()} - {red_tiles_coords[:,1].max()}")
print(f"First 3 red tile coordinates: \n{red_tiles_coords[0:3]}")

def visualize_grid(red_tiles_coords):
    """Visualizes the grid of red and blue tiles given the coordinates of red tiles."""
    max_x = red_tiles_coords[:,0].max()
    max_y = red_tiles_coords[:,1].max()
    
    grid_width = max_x + 3      # +3 to provide some padding, like example given
    grid_height = max_y + 2     # +2 to provide some padding, like example given
    
    grid = np.full((grid_height, grid_width), '.')  # '.' for non-red tiles
    
    for x, y in red_tiles_coords:
        grid[y, x] = '#'  # '#' for red tiles
    
    for row in grid:
        print(" ".join(row))

visualize_grid(red_tiles_coords)