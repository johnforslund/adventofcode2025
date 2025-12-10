
#########################
##  Day 8: Playground  ##
#########################
# https://adventofcode.com/2025/day/8


##############
##  Part 1  ##
##############

# Imports
import numpy as np
import pandas as pd
import os

# Initializing variables
folder_path = "day_8"
file_name = "input.txt"
sample_file_name = "input_sample.txt"

with open(os.path.join(folder_path, sample_file_name), "r") as f:
    original_document = f.read()

# Splitting document into lines
original_document = original_document.split("\n")
# Splitting into list of lists, split by ","
original_document = [line.split(",") for line in original_document]
# Converting to numpy array for easier manipulation
original_array = np.array(original_document)
# Converting to pandas dataframe for even easier manipulation (if needed)
original_df = pd.DataFrame(data=original_array, columns=["X", "Y", "Z"])

# Checking input
print(f"Number of junction boxes: {original_df.shape[0]}")
print(f"Min & max X coordinate of junction box: {original_df['X'].min()} - {original_df['X'].max()}")
print(f"Min & max Y coordinate of junction box: {original_df['Y'].min()} - {original_df['Y'].max()}")
print(f"Min & max Z coordinate of junction box: {original_df['Z'].min()} - {original_df['Z'].max()}")
print(f"First 3 coordinates: \n{original_df.iloc[0:3]}")


# Add a column for Euclidean space from origo (0,0,0)
original_df["Distance_from_origin"] = np.sqrt(original_df["X"].astype(float)**2 +
                                              original_df["Y"].astype(float)**2 +
                                              original_df["Z"].astype(float)**2)

# Sorting by distance from origin
sorted_df = original_df.sort_values(by="Distance_from_origin").reset_index(drop=True)

# Add a column for distance from previous junction box
sorted_df["Distance_from_previous"] = sorted_df["Distance_from_origin"].diff().fillna(0)

# Modifying the first junction box to have Distance_from_previous as np.inf (to avoid issues with min function later)
sorted_df.at[0, "Distance_from_previous"] = np.inf

print(sorted_df.head(10))

# TODO This method doesn't work correctly; see note below


###############
##  Fix/Note ##
###############
# The approach above sorts by distance from origin and compares successive
# differences in that radial distance. That does NOT measure the actual
# Euclidean distance between two junction boxes. Two points can have very
# similar distances from the origin yet be far apart from each other.

# To find the two closest junction boxes, compute pairwise Euclidean
# distances between points (X, Y, Z) and take the minimum.

# Convert coordinates to a numeric numpy array of shape (n, 3)
coords = original_df[["X", "Y", "Z"]].astype(float).to_numpy()
n = coords.shape[0]

# Compute all pairwise distances efficiently using broadcasting
# dist[i, j] = ||coords[i] - coords[j]||_2
diffs = coords[:, None, :] - coords[None, :, :]     # Differences in each coordinate to all other junction boxes
pairwise_dist = np.sqrt(np.sum(diffs**2, axis=2))   # Euclidean distances to all other junction boxes

# Mask out diagonal and duplicate pairs; consider only upper triangle
mask = np.triu(np.ones((n, n), dtype=bool), k=1)
upper_dists = np.where(mask, pairwise_dist, np.inf)

############################
##  Nearest-Neighbor Pair ##
############################

def nearest_neighbor_indices(upper_dists: np.ndarray) -> np.ndarray:
    # Find overall closest pair once (upper triangle min)
    nn_list = []
    for x in range(n):
        flat_min_idx = np.argmin(upper_dists[x])
        nn_list.append(flat_min_idx)
        #i_min, j_min = np.unravel_index(flat_min_idx, upper_dists.shape)
        #closest_row_i = original_df.iloc[i_min]
        #closest_row_j = original_df.iloc[j_min]
        #closest_distance = upper_dists[i_min, j_min]
    # Convert to numpy array
    return np.array(nn_list)


print("\nClosest pair by Euclidean distance between junction boxes:")
print(f"Row indices: {i_min} and {j_min}")
print(f"Coordinates A: {int(closest_row_i['X'])}, {int(closest_row_i['Y'])}, {int(closest_row_i['Z'])}")
print(f"Coordinates B: {int(closest_row_j['X'])}, {int(closest_row_j['Y'])}, {int(closest_row_j['Z'])}")
print(f"Euclidean distance between A and B: {closest_distance:.6f}")

########################################
##  Build Groups via Nearest Neighbors ##
########################################
# For each box, connect it to its single nearest neighbor.
# Then merge connections into groups using union-find.

def nearest_neighbor_indices(dist_matrix: np.ndarray) -> np.ndarray:
    # Set diagonal to inf to ignore self
    with np.errstate(invalid='ignore'):
        np.fill_diagonal(dist_matrix, np.inf)
    # Argmin per row gives nearest neighbor index for each node
    return np.argmin(dist_matrix, axis=1)

nn = nearest_neighbor_indices(upper_dists)

# Union-Find (Disjoint Set Union) implementation
parent = list(range(n))
rank = [0] * n

def find(x: int) -> int:
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a: int, b: int) -> None:
    ra, rb = find(a), find(b)
    if ra == rb:
        return
    if rank[ra] < rank[rb]:
        parent[ra] = rb
    elif rank[ra] > rank[rb]:
        parent[rb] = ra
    else:
        parent[rb] = ra
        rank[ra] += 1

# Create edges from each node to its nearest neighbor and union them
for i in range(n):
    j = nn[i]
    union(i, j)

# Collect groups
groups = {}
for i in range(n):
    r = find(i)
    groups.setdefault(r, []).append(i)

print("\nGroups of connected junction boxes (via nearest-neighbor unions):")
for root, members in groups.items():
    coords_list = [
        (
            int(original_df.iloc[idx]['X']),
            int(original_df.iloc[idx]['Y']),
            int(original_df.iloc[idx]['Z'])
        ) for idx in members
    ]
    print(f"Group root {root} | size {len(members)} | indices {members}")
    print(f"  Coordinates: {coords_list}")

# Get the three highest group sizes
group_sizes = sorted([len(members) for members in groups.values()], reverse=True)
top_3_sizes = group_sizes[:3]

# Multiply the sizes of the three largest groups
top_3_multiplied = np.prod(top_3_sizes)

