
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

# Find indices of the minimum distance pair
flat_min_idx = np.argmin(upper_dists)
i_min, j_min = np.unravel_index(flat_min_idx, upper_dists.shape)

closest_row_i = original_df.iloc[i_min]
closest_row_j = original_df.iloc[j_min]
closest_distance = upper_dists[i_min, j_min]

print("\nClosest pair by Euclidean distance between junction boxes:")
print(f"Row indices: {i_min} and {j_min}")
print(f"Coordinates A: {int(closest_row_i['X'])}, {int(closest_row_i['Y'])}, {int(closest_row_i['Z'])}")
print(f"Coordinates B: {int(closest_row_j['X'])}, {int(closest_row_j['Y'])}, {int(closest_row_j['Z'])}")
print(f"Euclidean distance between A and B: {closest_distance:.6f}")

