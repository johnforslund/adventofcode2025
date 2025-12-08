
###########################
##  Day 7: Laboratories  ##
###########################
# https://adventofcode.com/2025/day/7


##############
##  Part 1  ##
##############

# Imports
import numpy as np
import os


##################
###   Part 1   ###
##################

# Initializing variables
folder_path = "day_7"
file_name = "input.txt"
sample_file_name = "input_sample.txt"

with open(os.path.join(folder_path, sample_file_name), "r") as f:
    original_document = f.read()

# Splitting document into lines
original_document = original_document.split("\n")
# Converting to numpy array for easier manipulation
original_array = np.array([list(line) for line in original_document])

# Checking input
print(f"Number of problems: {len(original_document)}")
print(f"Length of first row: {len(original_document[0])}")
print(f"Length of last row: {len(original_document[-1])}")

# Finding the index of the starting point "S"
modified_array = original_array.copy()

# Set starting S symbol as | instead, for consistency
modified_array[0, np.where(modified_array[0] == "S")[0][0]] = "|"

# Initialize counter for when beam is split
split_counter = 0

# Go down the lines:
for i in range(1, modified_array.shape[0]):
    beam_mask = modified_array[i-1] == "|"  # Creating a numpy mask where (index/indices) the beam is present in the previous row
    all_available = modified_array[i] != "^"  # Checking if the candidate positions in the current row are not blocked by a "^"
    beam_available = beam_mask & all_available   # Candidate positions where the beam can go down without splitting
    beam_splitting = beam_mask & ~beam_available   # Candidate positions where the beam would need to split (i.e. blocked directly below)
    
    # Counting the splits (the True values in beam_splitting)
    split_counter += np.sum(beam_splitting)

    # Set the beam in the current row only where the candidate positions are available (not blocked)
    modified_array[i, beam_available] = "|"

    # Set the beams to the left and right of the non-available positions (i.e. with "^") if possible
    left = np.zeros_like(beam_splitting, dtype=bool)      # left: shift blocked one position toward lower indices (no wrap)
    left[:-1] = beam_splitting[1:]
    right = np.zeros_like(beam_splitting, dtype=bool)     # right: shift blocked one position toward higher indices (no wrap)
    right[1:] = beam_splitting[:-1]

    left &= all_available      # Ensure that left positions are available
    right &= all_available     # Ensure that right positions are available
    
    # Sets the (available) left and right positions to "|"
    modified_array[i, left | right] = "|"   


print(f"Number of splits: {split_counter}")


##################
###   Part 2   ###
##################

# Changes:
# The beam now goes left OR right when going through a splitter.
# Every time the beam DOESNT go left OR right (but it is possible) creates a new timeline.
# We need to count all possible timelines.

# Initializing variables
folder_path = "day_7"
file_name = "input.txt"
sample_file_name = "input_sample.txt"

with open(os.path.join(folder_path, sample_file_name), "r") as f:
    original_document = f.read()

# Splitting document into lines
original_document = original_document.split("\n")

# Converting to numpy array for easier manipulation
original_array = np.array([list(line) for line in original_document])

# Checking input
print(f"Number of problems: {len(original_document)}")
print(f"Length of first row: {len(original_document[0])}")
print(f"Length of last row: {len(original_document[-1])}")

# Finding the index of the starting point "S"
modified_array = original_array.copy()

# Set starting S symbol as | instead, for consistency
modified_array[0, np.where(modified_array[0] == "S")[0][0]] = "|"

# Initialize counter for when beam is split
split_counter = 0

# Initialize number of timelines
num_timelines = 1


# Prepare for counts[j] = number of timelines that have a beam at column j in the current row
nrows, ncols = modified_array.shape
start_idx = np.where(modified_array[0] == "|")[0][0]

counts = [0] * ncols
counts[start_idx] = 1

split_counter = 0

for i in range(1, nrows):
    all_available = modified_array[i] != "^"      # positions that can accept a beam straight down / be occupied
    next_counts = [0] * ncols                 # prepare next row counts

    # For visualization/union of reachable positions across all timelines:
    row_any_beam = np.zeros(ncols, dtype=bool)

    for j, c in enumerate(counts):
        if c == 0:          # skip columns with no possible timelines
            continue
        if all_available[j]:    # beam goes straight down (no split)
            next_counts[j] += c     # all c timelines go straight down
            row_any_beam[j] = True  # mark this position as having a beam in at least one timeline
        else:       # cell below is blocked
            # beam cannot go straight; try left and/or right
            left_added = False
            right_added = False
            if j - 1 >= 0 and all_available[j - 1]:     # can go left
                next_counts[j - 1] += c     # all c timelines go left
                row_any_beam[j - 1] = True  # mark this position as having a beam in at least one timeline
                left_added = True           # mark that we added left
            if j + 1 < ncols and all_available[j + 1]:     # can go right
                next_counts[j + 1] += c     # all c timelines go right
                row_any_beam[j + 1] = True  # mark this position as having a beam in at least one timeline
                right_added = True          # mark that we added right
            # count this as a split event if there was at least one blocked-down beam here
            if left_added or right_added:
                # If both sides available, this beam's timelines doubled (counts duplicated across two targets).
                # Count this as a split occurrence for diagnostics.
                split_counter += 1

    # Update modified_array row to show union of reachable positions (not necessary for counting timelines)
    modified_array[i, row_any_beam] = "|"

    counts = next_counts    # Move to next row

num_timelines = sum(counts)     # Total timelines is sum of all timelines reaching the last row
print(f"Number of splits: {split_counter}")
print(f"Number of timelines: {num_timelines}")
