
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

with open(os.path.join(folder_path, file_name), "r") as f:
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


# To find the two closest junction boxes, compute pairwise Euclidean
# distances between points (X, Y, Z) and take the minimum.

# Convert coordinates to a numeric numpy array of shape (n, 3)
coords = original_df[["X", "Y", "Z"]].astype(float).to_numpy()
n = coords.shape[0]

# Compute all pairwise distances efficiently using broadcasting
diffs = coords[:, None, :] - coords[None, :, :]     # Differences in each coordinate to all other junction boxes

pairwise_dist = np.sqrt(np.sum(diffs**2, axis=2))   # Euclidean distances to all other junction boxes
np.fill_diagonal(pairwise_dist, np.inf)             # Set diagonal to infinity to ignore self-distances


###############
##   Part 1  ##
###############

df = original_df.copy()
df["NN_Index"] = -1
df["NN_Distance"] = np.inf
df["Group_ID"] = -1
groups = {}

for i in range(n//2):
    # Find nearest neighbor for each junction box
    df["NN_Index"] = np.argmin(pairwise_dist, axis=1)
    df["NN_Distance"] = np.min(pairwise_dist, axis=1)

    # Fetch row with closest distance
    min_distance_row = df[df.NN_Distance == df.NN_Distance.min()].iloc[0]
    A_index = int(min_distance_row.name)
    B_index = int(min_distance_row["NN_Index"])
    group_id = int()

    # Check if either box is already assigned to a group
    A_group = int(df.iloc[A_index].Group_ID)
    B_group = int(df.iloc[B_index].Group_ID)
    print(f"Connecting box {A_index} (group {A_group}) and box {B_index} (group {B_group}) with distance {min_distance_row.NN_Distance}")
    if A_group == -1 and B_group == -1:
        # Neither box is in a group already, create new group
        group_id = len(groups)      # Begins at 0, then 1 etc
        groups[group_id] = [A_index, B_index]
        df.loc[groups[group_id], "Group_ID"] = group_id
    elif A_group != -1 and B_group == -1:
        # A is in a group, B is not - add B to A's group
        group_id = A_group
        groups[group_id].append(B_index)
        df.loc[B_index, "Group_ID"] = group_id
    elif A_group == -1 and B_group != -1:
        # B is in a group, A is not - add A to B's group
        group_id = B_group
        groups[group_id].append(A_index)
        df.loc[A_index, "Group_ID"] = group_id
    else:
        # Both are already in groups - combine them into A's group unless they are the same
        if A_group != B_group:
            # Merge B's group into A's group
            group_id = A_group
            for idx in groups[B_group]:
                groups[group_id].append(idx)
                df.loc[idx, "Group_ID"] = group_id
            del groups[B_group]

    # Set their pairwise distance to infinity to avoid re-selection
    pairwise_dist[A_index, B_index] = np.inf
    pairwise_dist[B_index, A_index] = np.inf



# Get the three highest group sizes
group_sizes = sorted([len(members) for members in groups.values()], reverse=True)
top_3_sizes = group_sizes[:3]

# Multiply the sizes of the three largest groups
top_3_multiplied = np.prod(top_3_sizes)


