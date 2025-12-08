
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

# Initializing variables
folder_path = "day_7"
file_name = "input.txt"
sample_file_name = "input_sample.txt"

with open(os.path.join(folder_path, file_name), "r") as f:
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