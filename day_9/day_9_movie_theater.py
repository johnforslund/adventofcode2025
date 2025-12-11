
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
        green_tiles.extend(
            (x_a, y)
            for y in range(min(y_a, y_b), max(y_a, y_b) + 1)
        )
        # Create green tiles in a straight line between (x_a, y_a) and (x_b, y_a)
        green_tiles.extend(
            (x, y_a)
            for x in range(min(x_a, x_b), max(x_a, x_b) + 1)
        )
    green_tile_coords = np.array(green_tiles)
    return green_tile_coords


def fill_in_green_tiles(red_tile_coords, green_tile_line_coords):
        # Fill in the gaps on each row only between the first and last Red/Green tiles
        green_tile_list = list(green_tile_line_coords)
        red_x_min = red_tile_coords[:,0].min()
        red_x_max = red_tile_coords[:,0].max()
        red_y_min = red_tile_coords[:,1].min()
        red_y_max = red_tile_coords[:,1].max()
        #red_set = set(map(tuple, red_tile_coords))
        green_set = set(map(tuple, green_tile_line_coords))
        for y in range(red_y_min, red_y_max + 1):
            # Find all x on this row that are already Red or Green
            line_xs = [x for x in range(red_x_min, red_x_max + 1)
                       if (x, y) in green_set]
            if len(line_xs) < 2:
                continue  # nothing to fill on this row
            x_start = min(line_xs)
            x_end = max(line_xs)
            for x in range(x_start, x_end + 1):
                coord = (x, y)
                if coord not in green_set:
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


def visualize_grid_with_dict(red_tile_coords, green_tile_line_coords_dict):
    """Visualizes the grid of red and non-red tiles given the coordinates of red tiles.
    Optionally also includes green tiles in a dictionary.
    Output is the printed grid."""
    max_x = red_tile_coords[:,0].max()
    max_y = red_tile_coords[:,1].max()
    
    grid_width = max_x + 3      # +3 to provide some padding, like example given
    grid_height = max_y + 2     # +2 to provide some padding, like example given
    
    grid = np.full((grid_height, grid_width), '.')  # '.' for non-red tiles
    
    for x, y in red_tile_coords:
        grid[y, x] = '#'  # '#' for red tiles

    if green_tile_line_coords_dict is not False:
        for y, (x_min, x_max) in green_tile_line_coords_dict.items():
            for x in range(x_min, x_max + 1):
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


def calculate_largest_rectangle_with_dict(red_tile_coords, limited_by_green_tiles=False, green_tile_line_coords_dict=False):
    """Calculates the area of the largest rectangle that can be formed
    using two red tiles as opposite corners.
    
    If limited_by_green_tiles is True, only considers rectangles
    that ONLY include green tiles (green_tile_line_coords_dict) within their area.
    """
    max_area = 0
    
    n = red_tile_coords.shape[0]
    
    if limited_by_green_tiles and green_tile_line_coords_dict is False:
        print("Error: limited_by_green_tiles is True but no green_tile_line_coords_dict provided.")
        return 0
    
    elif limited_by_green_tiles and green_tile_line_coords_dict is not False:
        
        for i in range(n):
            for j in range(i + 1, n):

                x1, y1 = red_tile_coords[i]
                x2, y2 = red_tile_coords[j]
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                
                # Check if all tiles within the rectangle are green tiles
                all_green = False
                x_min, x_max = green_tile_line_coords_dict["x"][y1][0], green_tile_line_coords_dict["x"][y1][1]
                y_min, y_max = green_tile_line_coords_dict["y"][x1][0], green_tile_line_coords_dict["y"][x1][1]
                if x_min <= x1 <= x_max:
                    if x_min <= x2 <= x_max:
                        if y_min <= y1 <= y_max:
                            if y_min <= y2 <= y_max:
                                all_green = True
                if all_green:
                    max_area = max(max_area, area)
                #range_x = range(green_tile_line_coords_dict["x"][y1][0], green_tile_line_coords_dict["x"][y1][1] + 1)
                #if x1 not in range_x or x2 not in range_x:
                #    all_green = False
                """
                range_y = range(green_tile_line_coords_dict["y"][x1][0], green_tile_line_coords_dict["y"][x1][1] + 1)
                if y1 not in range_y or y2 not in range_y:
                    all_green = False
                if all_green:
                    max_area = max(max_area, area)
                """
        """
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = red_tile_coords[i]
                x2, y2 = red_tile_coords[j]
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                
                # Check if all tiles within the rectangle are green tiles
                all_green = True
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    if y not in green_tile_line_coords_dict:
                        all_green = False
                        break
                    x_min, x_max = green_tile_line_coords_dict[y]
                    if x_min > min(x1, x2) or x_max < max(x1, x2):
                        all_green = False
                        break
                
                if all_green:
                    max_area = max(max_area, area)
            """
    else:
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = red_tile_coords[i]
                x2, y2 = red_tile_coords[j]
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                max_area = max(max_area, area)
    
    return max_area


# Part 1: Largest rectangle using any red tiles
grid = visualize_grid(red_tile_coords)
largest_rect = calculate_largest_rectangle(red_tile_coords, grid, limited_by_green_tiles=False)
print(f"Part 1: Largest rectangle area: {largest_rect}")

# Part 2: Largest rectangle using only green tiles between red tiles
green_tile_line_coords = create_green_tile_line_coords(red_tile_coords)
#grid = visualize_grid(red_tile_coords, green_tile_line_coords)


# Create green_tile_line_coords_dict that maps each row AND column to the list of green tiles on that row
# e.g. {y1: [x1, x2, x3], y2: [x4, x5], ...} and vice versa
# and also reduce the values to a minimum and maximum x coordinate only for faster filling in of green tiles
ys = green_tile_line_coords[:, 1]
xs = green_tile_line_coords[:, 0]

# Sort by y so we can group rows efficiently
ys_order = np.argsort(ys)
ys_sorted_by_y = ys[ys_order]
xs_sorted_by_y = xs[ys_order]

xs_order = np.argsort(xs)
ys_sorted_by_x = ys[xs_order]
xs_sorted_by_x = xs[xs_order]

# Find group boundaries for each unique y
unique_y, y_idx_start = np.unique(ys_sorted_by_y, return_index=True)
y_idx_end = np.r_[y_idx_start[1:], ys_sorted_by_y.size]

# Find group boundaries for each unique x
unique_x, x_idx_start = np.unique(xs_sorted_by_x, return_index=True)
x_idx_end = np.r_[x_idx_start[1:], xs_sorted_by_x.size]

# Compute min/max x per y using vectorized reductions
x_min = np.minimum.reduceat(xs_sorted_by_y, y_idx_start)
x_max = np.maximum.reduceat(xs_sorted_by_y, y_idx_start)

# Compute min/max y per x using vectorized reductions
y_min = np.minimum.reduceat(ys_sorted_by_x, x_idx_start)
y_max = np.maximum.reduceat(ys_sorted_by_x, x_idx_start)

# Build dict: only for rows that actually have green tiles
green_tile_line_coords_dict = {}
green_tile_line_coords_dict["x"] = {
    int(y): (int(xmin), int(xmax)) for y, xmin, xmax in zip(unique_y, x_min, x_max)
}
green_tile_line_coords_dict["y"] = {
    int(x): (int(ymin), int(ymax)) for x, ymin, ymax in zip(unique_x, y_min, y_max)
}

#grid = visualize_grid_with_dict(red_tile_coords, green_tile_line_coords_dict)

#green_tile_filled_coords_with_dict = fill_in_green_tiles_with_dict(red_tile_coords, green_tile_line_coords_dict)


#green_tile_filled_coords = fill_in_green_tiles(red_tile_coords, green_tile_line_coords)
#grid = visualize_grid(red_tile_coords, green_tile_filled_coords)

#largest_rect = calculate_largest_rectangle(red_tile_coords, grid, limited_by_green_tiles=True, green_tile_coords=green_tile_filled_coords)
largest_rect = calculate_largest_rectangle_with_dict(red_tile_coords, limited_by_green_tiles=True, green_tile_line_coords_dict=green_tile_line_coords_dict)




print(f"Part 2: Largest rectangle area: {largest_rect}")

# 4635268638 is too high.