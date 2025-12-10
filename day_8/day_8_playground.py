
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

class UnionFind:
    """
    A union-find (disjoint-set) data structure with path-compression and union by size.
    """
    def __init__(self, n):
        # Initialize n disjoint sets
        self.parent = list(range(n))
        self.size = [1] * n
    def find(self, a):
        # Find root of set containing a
        # with path-compression, find root
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a
    def union(self, a, b):
        # Union two sets, return False if already in the same set
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # Union by size, attach smaller tree to larger tree
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True
    def groups(self):
        # Return a dictionary of root -> list of members
        roots = {}
        for i in range(len(self.parent)):
            r = self.find(i)
            roots.setdefault(r, []).append(i)
        return roots
    

uf = UnionFind(n)

for i in range(n):
    # Find nearest neighbor for each junction box
    df["NN_Index"] = np.argmin(pairwise_dist, axis=1)
    df["NN_Distance"] = np.min(pairwise_dist, axis=1)

    # Fetch row with closest distance
    min_distance_row = df[df.NN_Distance == df.NN_Distance.min()].iloc[0]
    A_index = int(min_distance_row.name)
    B_index = int(min_distance_row["NN_Index"])
    group_id = int()

    # Check if either box is already assigned to a group
    # Use union-find to merge clusters safely (and easier)
    A_group = int(df.iloc[A_index].Group_ID)
    B_group = int(df.iloc[B_index].Group_ID)
    print(f"Connecting box {A_index} (group {A_group}) and box {B_index} (group {B_group}) with distance {min_distance_row.NN_Distance}")
    uf.union(A_index, B_index)  # Union the two boxes(/groups)
    # Set Group_ID field to the current root for the two touched nodes
    root = int(uf.find(A_index))
    df.loc[[A_index, B_index], "Group_ID"] = root

    # Set their pairwise distance to infinity to avoid re-selection
    pairwise_dist[A_index, B_index] = np.inf
    pairwise_dist[B_index, A_index] = np.inf


# Get the three highest group sizes (only consider groups of size >= 2 to match previous behaviour)
uf_groups = uf.groups()
group_sizes = sorted([len(members) for members in uf_groups.values() if len(members) >= 2], reverse=True)
top_3_sizes = group_sizes[:3]

# Multiply the sizes of the three largest groups
top_3_multiplied = np.prod(top_3_sizes)

print(f"Sizes of the three largest groups: {top_3_sizes}")
print(f"Product of sizes of the three largest groups: {top_3_multiplied}")