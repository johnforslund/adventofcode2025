

########################
##  Day 5: Cafeteria  ##
########################
# https://adventofcode.com/2025/day/5


##############
##  Part 1  ##
##############

# Imports
#import numpy as np
import os

# Initializing variables
#folder_path = os.path.dirname(os.path.abspath(__file__))   # TODO: Not working when running from REPL
folder_path = "day_5"
file_name = "input.txt"
sample_file_name = "input_sample.txt"

# Reading sample file
with open(os.path.join(folder_path, sample_file_name), "r") as f:
    document = f.read()

# Splitting document into fresh batches (first lines with ranges, then blank line, then lines with IDs)
document = document.split("\n\n")
doc_fresh = document[0].splitlines()                    # Keep as strings for now ("3-5" etc) for easier readability
doc_ids = [int(x) for x in document[1].splitlines()]    # Convert to integers (e.g. 5)


# Checking input
print(f"Number of fresh ID ranges: {len(doc_fresh)}")
print(f"Number of IDs to check: {len(doc_ids)}")
print(f"First 5 fresh ID ranges: {doc_fresh[:5]}")
print(f"First 5 IDs to check: {doc_ids[:5]}")

# Document provides ranges of fresh IDs, e.g. "3-5" means IDs 3, 4, and 5 are fresh (Note: inclusive, and can overlap),
# as well as a list of IDs to check. Need to count how many of the IDs to check are fresh (within the ranges, note: within ANY range, as they can overlap).
# If they aren't in a fresh ID range, they are spoiled.

# Output is the number of fresh ingredient IDs.

# Note: Possible functionality options:
# [X] Turn on/off inclusive ranges on both ends (e.g. "3-5" means 3, 4 or 4, 5, or just 5)
# [/] #TODO WIP, see branch feature/allow-overlaps. Turn on/off allowing overlapping ranges (if ranges overlap, remove them)
# [ ] Turn on/off accumulating overlapping ranges (if ranges overlap, count IDs within them as fresh multiple times)
# [X] Allow the possibility of ranges not being in order (e.g. "1-3", "5-3", "2-4" etc)
# [-] Convert ranges to sets for faster checking (scratched due to not holding duplicates - Counter or even better merge + bisect could be used, but probably not worth it)


def parse_range_ids(doc_fresh: list[str], incl_start: bool = True, incl_end: bool = True) -> list[range]:
    """Parse the fresh ID ranges from the document (list of strings) into a list of range objects.
    
    Args:
        doc_fresh (list of str): List of fresh ID ranges as strings.
        incl_start (bool): Whether the start of the range is inclusive.
        incl_end (bool): Whether the end of the range is inclusive.
    
    Returns:
        fresh_ranges (list of ranges): List of range objects representing fresh ID ranges.
    """
    # Initialize variables
    fresh_ranges = []       # Create empty list, to hold ranges (e.g. range(start, end))
    adj_start = 0 if incl_start else 1
    adj_end = 1 if incl_end else 0

    # Parse each range string into a range object
    for r in doc_fresh:
        start, end = r.split("-")           # Split from e.g. "3-5" to "3", "5"
        start, end = int(start), int(end)   # Convert to integers e.g. 3, 5
        if start > end:
            start, end = end, start           # Swap to ensure start <= end
        fresh_ranges.append(range(start + adj_start, end + adj_end))  # Create range (inclusive, so end + 1)
        
    return fresh_ranges


def check_all_ids(doc_ids: list[int], fresh_ranges: list[range]) -> int:
    """Check all IDs against the fresh ID ranges and count how many are fresh.

    Args:
        doc_ids (list of int): List of IDs to check.
        fresh_ranges (list of ranges): List of fresh ID ranges.

    Returns:
        int: Number of fresh IDs.
    """
    fresh_count = 0
    for id_to_check in doc_ids:
        if check_id_status(id_to_check, fresh_ranges):
            fresh_count += 1

    return fresh_count


def check_id_status(id_to_check: int, fresh_ranges: list[range]) -> bool:
    """Check if a given ID is fresh or spoiled based on the provided fresh ID ranges.

    Args:
        id_to_check (int): The ID to check.
        fresh_ranges (list of ranges): List of fresh ID ranges.

    Returns:
        bool: True if the ID is fresh, False if it is spoiled.
    """
    for r in fresh_ranges:
        if id_to_check in r:
            return True  # ID is fresh

    return False  # ID is spoiled





fresh_ranges = parse_range_ids(doc_fresh, incl_start=True, incl_end=True)
fresh_count = check_all_ids(doc_ids, fresh_ranges)
print(f"Number of fresh IDs: {fresh_count}")



##############
##  Part 2  ##
##############


# Change:
# Goal is to find all of the ID's that are considered fresh based on the fresh ID ranges.

def get_all_ids_from_fresh_ranges(fresh_ranges: list[range]) -> tuple[set[int], int]:
    """Get all IDs that are considered fresh based on the provided fresh ID ranges.

    Args:
        fresh_ranges (list of ranges): List of fresh ID ranges.

    Returns:
        set of int: Set of all fresh IDs,
        int: Count of all fresh IDs in set.
    """
    fresh_id_set = set()
    for r in fresh_ranges:
        fresh_id_set.update(range(r.start, r.stop))  # Add all IDs in range to set

    fresh_id_count = len(fresh_id_set)

    return fresh_id_set, fresh_id_count


fresh_id_set, fresh_id_count = get_all_ids_from_fresh_ranges(fresh_ranges)
print(f"All fresh IDs {sorted(fresh_id_set)}")
print(f"Number of all fresh IDs: {fresh_id_count}")