
############################
##  Day 9: Movie Theater  ##
############################
# https://adventofcode.com/2025/day/9


##############
##  Part 1  ##
##############

# Imports
import numpy as np
import os

# Initializing variables
folder_path = "day_9"
file_name = "input.txt"
sample_file_name = "input_sample.txt"

with open(os.path.join(folder_path, file_name), "r") as f:
    original_document = f.read()

# Splitting document into lines
original_document = original_document.split("\n")
# Splitting into list of tuples of ints
original_document = [tuple(int(x) for x in line.split(",")) for line in original_document]
# Converting to numpy array for easier manipulation
red_tile_coords = np.array(original_document)

print(f"Number of red tile coordinates: {red_tile_coords.shape[0]}")
print(f"Min & max X coordinate of red tile: {red_tile_coords[:,0].min()} - {red_tile_coords[:,0].max()}")
print(f"Min & max Y coordinate of red tile: {red_tile_coords[:,1].min()} - {red_tile_coords[:,1].max()}")
print(f"First 3 red tile coordinates: \n{red_tile_coords[0:3]}")



def create_green_tile_line_coords(red_tile_coords):
    """Creates the coordinates of green tiles based on the red tile coordinates.
    Green tiles are created in a straight line between any adjacent (before & after) red tiles in the (ordered & wrapping) list."""
    green_tiles = []
    n = red_tile_coords.shape[0]
    for i in range(n):
        x0, y0 = red_tile_coords[i - 1]  # Previous red tile, wrapping around
        x1, y1 = red_tile_coords[i]
        x2, y2 = red_tile_coords[(i + 1) % n]  # Next red tile, wrapping around
        if x0==x1:
            x_a = x0
            x_b = x2
        elif x1==x2:
            x_a = x1
            x_b = x0
        else:
            print("Error: No duplicate x coordinate found")
        
        if y0==y1:
            y_a = y0
            y_b = y2
        elif y1==y2:
            y_a = y1
            y_b = y0
        else:
            print("Error: No duplicate y coordinate found")

        # Create green tiles in a straight line between (x_a, y_a) and (x_a, y_b)
        for y in range(min(y_a, y_b), max(y_a, y_b) + 1):
            if (x_a, y) not in map(tuple, red_tile_coords):
                if (x_a, y) not in green_tiles:
                    green_tiles.append((x_a, y))
        # Create green tiles in a straight line between (x_a, y_a) and (x_b, y_a)
        for x in range(min(x_a, x_b), max(x_a, x_b) + 1):
            if (x, y_a) not in map(tuple, red_tile_coords):
                if (x, y_a) not in green_tiles:
                    green_tiles.append((x, y_a))

    green_tile_coords = np.array(green_tiles)
    return green_tile_coords


def fill_in_green_tiles(red_tile_coords, green_tile_coords):
        # Fill in the gaps on each row only between the first and last Red/Green tiles
        green_tile_list = list(green_tile_coords)
        red_x_min = red_tile_coords[:,0].min()
        red_x_max = red_tile_coords[:,0].max()
        red_y_min = red_tile_coords[:,1].min()
        red_y_max = red_tile_coords[:,1].max()
        red_set = set(map(tuple, red_tile_coords))
        green_set = set(map(tuple, green_tile_coords))
        for y in range(red_y_min, red_y_max + 1):
            # Find all x on this row that are already Red or Green
            line_xs = [x for x in range(red_x_min, red_x_max + 1)
                       if (x, y) in red_set or (x, y) in green_set]
            if len(line_xs) < 2:
                continue  # nothing to fill on this row
            x_start = min(line_xs)
            x_end = max(line_xs)
            for x in range(x_start, x_end + 1):
                coord = (x, y)
                if coord not in red_set and coord not in green_set:
                    green_tile_list.append(coord)
                    green_set.add(coord)
        green_tile_filled_coords = np.array(green_tile_list)
        return green_tile_filled_coords
        


def visualize_grid(red_tile_coords, green_tile_coords=False):
    """Visualizes the grid of red and non-red tiles given the coordinates of red tiles.
    Optionally also includes green tiles.
    Output is the printed grid."""
    max_x = red_tile_coords[:,0].max()
    max_y = red_tile_coords[:,1].max()
    
    grid_width = max_x + 3      # +3 to provide some padding, like example given
    grid_height = max_y + 2     # +2 to provide some padding, like example given
    
    grid = np.full((grid_height, grid_width), '.')  # '.' for non-red tiles
    
    for x, y in red_tile_coords:
        grid[y, x] = '#'  # '#' for red tiles

    if green_tile_coords is not False:
        for x, y in green_tile_coords:
            grid[y, x] = 'G'  # 'G' for green tiles

    for row in grid:
        print(" ".join(row))
    return grid


# Calculate the largest rectangle possible using two red tiles as opposite corners
def calculate_largest_rectangle(red_tile_coords, grid, limited_by_green_tiles=False, green_tile_coords=False):
    """Calculates the area of the largest rectangle that can be formed
    using two red tiles as opposite corners.
    
    If limited_by_green_tiles is True, only considers rectangles
    that ONLY include green tiles (green_tile_coords) within their area.
    """
    max_area = 0
    
    n = red_tile_coords.shape[0]
    
    if limited_by_green_tiles and green_tile_coords is False:
        print("Error: limited_by_green_tiles is True but no green_tile_coords provided.")
        return 0
    
    elif limited_by_green_tiles and green_tile_coords is not False:
        #green_tile_set = set(map(tuple, green_tile_coords)) # Set for faster lookup
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = red_tile_coords[i]
                x2, y2 = red_tile_coords[j]
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                
                # Check if all tiles within the rectangle are green tiles
                all_green = True
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    for y in range(min(y1, y2), max(y1, y2) + 1):
                        if grid[(y, x)] == ".":
                            all_green = False
                            break
                    if not all_green:
                        break
                
                if all_green:
                    max_area = max(max_area, area)
                    #print(f"Found rectangle with corners: ({x1}, {y1}), ({x2}, {y2}) -> Area: {area}")
                    #print(f"Max area so far: {max_area}")

    else:
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = red_tile_coords[i]
                x2, y2 = red_tile_coords[j]
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                max_area = max(max_area, area)
                #print(f"Found rectangle with corners: ({x1}, {y1}), ({x2}, {y2}) -> Area: {area}")
                #print(f"Max area so far: {max_area}")
    
    return max_area


green_tile_line_coords = create_green_tile_line_coords(red_tile_coords)
grid = visualize_grid(red_tile_coords, green_tile_line_coords)

green_tile_filled_coords = fill_in_green_tiles(red_tile_coords, green_tile_line_coords)
grid = visualize_grid(red_tile_coords, green_tile_filled_coords)

largest_rect = calculate_largest_rectangle(red_tile_coords, grid, limited_by_green_tiles=True, green_tile_coords=green_tile_filled_coords)
print(f"Largest rectangle area: {largest_rect}")
