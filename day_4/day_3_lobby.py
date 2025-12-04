

##################################
##  Day 4: Printing Department  ##
##################################
# https://adventofcode.com/2025/day/4


##############
##  Part 1  ##
##############

# Imports
import numpy as np

"""
# Reading sample file
with open("day_4/input_sample.txt", "r") as f:
    document = f.read().split()
"""

# Reading file
with open("day_4/input.txt", "r") as f:
    document = f.read().split()

# Creating it as a numpy array for easier visualization and manipulation (if needed)
original_grid = np.array([list(row) for row in document])

# Checking input
print(f"Size of grid: {original_grid.shape[0]} rows x {original_grid.shape[1]} columns")
print(f"Total number of rolls: {(original_grid == "@").sum()}")
print(f"Total number of empty spaces: {(original_grid == ".").sum()}")
print(f"Grid: \n{original_grid}")

# Given a grid of X rows and Y columns, where each space is either empty (.) or has a roll (@),
# determine how many rolls of paper can be accessed by the forklist.

# The forklist can only access a roll of paper if there are fewer than four rolles of paper
# in the eight adjacent positions (horizontally, vertically, and diagonally).
# Assumption 1 based on sample: it should not be calculated sequentially nor iteratively, but as the grid is at the start.
# Assumption 2 based on sample: a space outside the grid is considered empty (.), it does not roll over to the other side.
# ^ possibly part 2?

# Output is the total number of rolls that can be accessed by the forklist.


def count_accessible_rolls(grid, sequential_removal=False, iterative_removal=False, out_of_bounds_allowed=False, adjacency_limit=1, include_diagonal=True):
    # Initialize variables
    updated_grid = grid.copy()
    total_accessible_rolls = 0

    # Creating direction indices for the adjacent positions
    adjacent_positions = []
    for a in range(1, adjacency_limit+1):
        adjacent_positions.extend([(a,0), (-a,0), (0,a), (0,-a)])
        if include_diagonal:
            adjacent_positions.extend([(a,a), (a,-a), (-a,a), (-a,-a)])
    
    # Iterate through every space in the grid
    if iterative_removal:   # i.e. checking the grid multiple times until no more rolls can be accessed
        print("Iterative removal activated")
        previous_total_accessible_rolls = -1
        while total_accessible_rolls != previous_total_accessible_rolls:
            print("While loop iteration started")
            previous_total_accessible_rolls = total_accessible_rolls
            print(f"Previous total accessible rolls: {previous_total_accessible_rolls}")
            accessible_rolls, updated_grid = _check_each_space(updated_grid, adjacent_positions, sequential_removal, iterative_removal, out_of_bounds_allowed)
            total_accessible_rolls += accessible_rolls
            print(f"New total accessible rolls: {total_accessible_rolls}")
    else:
        accessible_rolls, updated_grid = _check_each_space(updated_grid, adjacent_positions, sequential_removal, iterative_removal, out_of_bounds_allowed)
        total_accessible_rolls = accessible_rolls

    return total_accessible_rolls, updated_grid


def _check_each_space(updated_grid, adjacent_positions, sequential_removal, iterative_removal, out_of_bounds_allowed):
    rows, cols = updated_grid.shape
    accessible_rolls = 0
    for r in range(rows):
        for c in range(cols):
            if updated_grid[r,c] == "@":
                # Count adjacent rolls
                adjacent_rolls = 0
                for ar, ac in adjacent_positions:
                    nr, nc = r + ar, c + ac
                    if not out_of_bounds_allowed:
                        if not (0 <= nr < rows and 0 <= nc < cols):   # Checking bounds so not outside the grid
                            continue
                    if not sequential_removal and not iterative_removal:
                        if (updated_grid[nr, nc] == "@") or (updated_grid[nr, nc] == "X"):
                            adjacent_rolls += 1
                    else:
                        if updated_grid[nr, nc] == "@":
                            adjacent_rolls += 1
                # Check if the number of adjacent rolls is within the limit
                if adjacent_rolls < 4:
                    updated_grid[r,c] = "X"  # Mark as accessible
                    accessible_rolls += 1

    return accessible_rolls, updated_grid


accessible_rolls, updated_grid = count_accessible_rolls(original_grid)
print(f"Total number of accessible rolls: {accessible_rolls}")
print(f"Updated grid: \n{updated_grid}")



##############
##  Part 2  ##
##############


# Change: It should now be done iteratively until no more rolls can be accessed.
# Need to pass the parameter iterative_removal to the _count_accessible_rolls function as well... Then it works:
accessible_rolls, updated_grid = count_accessible_rolls(grid=original_grid, sequential_removal=False, iterative_removal=True)
print(f"Total number of accessible rolls: {accessible_rolls}")
print(f"Updated grid: \n{updated_grid}")

