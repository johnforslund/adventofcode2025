

##############################
##  Day 2: Gift Shop  ##
##############################
# https://adventofcode.com/2025/day/2



##############
##  Part 1  ##
##############

# Reading file
with open("day_2/input.txt", "r") as f:
    document = f.read().split(",")

# Checking input
print(f"Number of ID ranges: {len(document)}")
print(f"ID ranges increasing: {sum(1 for r in document if int(r.split('-')[1]) > int(r.split('-')[0]))}")
print(f"ID ranges decreasing: {sum(1 for r in document if int(r.split('-')[1]) < int(r.split('-')[0]))}")
print(f"First 10 ID ranges: {document[:10]}")

# Input consists of a series of ID ranges [A-B].
# A and B are positive integers, and A < B.

# Goal is to find invalid ID's within the ranges (incl. both A and B).
# An ID is invalid if it consists entirely of two repeated integers (e.g. 11, 2222, 123123 - note: 111 is valid) 
# => if ID = XX, where X is any integer.
# Note: This means an ID have to be even in length to be invalid.

# Output is a positive integer, consisting of the sum of all the invalid ID's (e.g. 11 + 2222 + 123123 = 125336).

# Initializing variables
invalid_id_list = []  # List of invalid ID's
invalid_id_sum = 0  # Sum of invalid ID's

for id_range in document:
    start_id = int(id_range.split('-')[0])
    end_id = int(id_range.split('-')[1])

    # Convert to string for working with first and second half easier, as well as lengths
    start_id_str = str(start_id)
    end_id_str = str(end_id)

    if (len(start_id_str) == len(end_id_str)) and (len(start_id_str) % 2 != 0):
        pass #continue  # All IDs in this range are odd in length, so skip to next range

    for n in range(len(start_id_str), len(end_id_str) + 1):     # Looping through lengths of IDs
        candidate_start = start_id
        candidate_start_str = str(candidate_start)

        candidate_end = end_id
        candidate_end_str = str(candidate_end)

        if n % 2 != 0:                                          # If first length is odd,
            continue                                            # Then skip it, continue with the loop

        if n > len(start_id_str):                               # If not the start length, i.e. if we moved from start length to higher lengths
            candidate_start = 10 ** (n - 1)                     # Then set new first ID to first integer of that length n (i.e. 100 for length 3, 1000 for length 4, etc.)
            candidate_start_str = str(candidate_start)

        if n < len(end_id_str):                                 # If not the end length, i.e. if we moved from end length to lower lengths
            candidate_end_str = "9" * n                         # Then set new last ID to last integer of that length n (i.e. 999 for length 3, 9999 for length 4, etc.)
            candidate_end = int(candidate_end_str)
        
        print(f"n: {n} out of {len(end_id_str)}")

        # Set the halfway index
        half_index = n / 2
        assert half_index.is_integer(), "Half index is not integer!"    # Sanity check
        half_index = int(half_index)
        print(f"half_index: {half_index}")

        candidate_half_id = candidate_start_str[:half_index]
        candidate_id = int(candidate_half_id * 2)               # Creating the first candidate ID by repeating the first half

        while candidate_id <= candidate_end:                    # Ensure it doesn't exceed the (candidate) end ID
            
            if candidate_id in (range(start_id, end_id + 1)):     # Last check if candidate ID is within the original start and end ID range
                invalid_id_list.append(candidate_id)
                print("Found invalid ID:", candidate_id)

            candidate_half_id = str(int(candidate_half_id) + 1)   # Incrementing the first half's first integer by 1
            candidate_id = int(candidate_half_id * 2)


invalid_id_sum = sum(invalid_id_list)
print(f"Output: {invalid_id_sum}")



##############
##  Part 2  ##
##############


# Same problem, but definitions of invalid ID's has changed:
# An ID is invalid if it consists entirely of two OR MORE repeated integers (e.g. 11, 222, 123123123, 99999)
# => if ID = XX[X...], where X is any integer.



# Initializing variables
invalid_id_list = {}  # List of invalid ID's
invalid_id_sum = 0  # Sum of invalid ID's

for d in range(len(document)):
    start_id = int(document[d].split('-')[0])
    end_id = int(document[d].split('-')[1])

    invalid_id_list[d] = []   # Initializing list for this range

    # Convert to string for working with first and second half easier, as well as lengths
    start_id_str = str(start_id)
    end_id_str = str(end_id)

    #if (len(start_id_str) == len(end_id_str)) and (len(start_id_str) % 2 != 0):
    #    pass #continue  # All IDs in this range are odd in length, so skip to next range

    for n in range(len(start_id_str), len(end_id_str) + 1):     # Looping through lengths of IDs
        candidate_start = start_id
        candidate_start_str = str(candidate_start)

        candidate_end = end_id
        candidate_end_str = str(candidate_end)

        #if n % 2 != 0:                                          # If first length is odd,
        #    continue                                            # Then skip it, continue with the loop

        if n > len(start_id_str):                               # If not the start length, i.e. if we moved from start length to higher lengths
            candidate_start = 10 ** (n - 1)                     # Then set new first ID to first integer of that length n (i.e. 100 for length 3, 1000 for length 4, etc.)
            candidate_start_str = str(candidate_start)

        if n < len(end_id_str):                                 # If not the end length, i.e. if we moved from end length to lower lengths
            candidate_end_str = "9" * n                         # Then set new last ID to last integer of that length n (i.e. 999 for length 3, 9999 for length 4, etc.)
            candidate_end = int(candidate_end_str)
        
        print(f"n: {n} out of {len(end_id_str)}")


        # Loop through different split indices
        for s in range(2, n + 1):                               # Looping through possible split sizes (s = number of repeats)
            split_index = n / s
            if not split_index.is_integer():
                continue                                        # Skip non-integer split sizes
            #assert split_index.is_integer(), "Split index is not integer!"    # Sanity check
            split_index = int(split_index)
            print(f"split_index: {split_index}")

            candidate_half_id = candidate_start_str[:split_index]
            candidate_id = int(candidate_half_id * s)               # Creating the first candidate ID by repeating the first half

            while candidate_id <= candidate_end:                    # Ensure it doesn't exceed the (candidate) end ID
                
                if candidate_id in (range(start_id, end_id + 1)):     # Last check if candidate ID is within the original start and end ID range
                    if candidate_id not in invalid_id_list[d]:
                        invalid_id_list[d].append(candidate_id)
                    print("Found invalid ID:", candidate_id)

                candidate_half_id = str(int(candidate_half_id) + 1)   # Incrementing the first half's first integer by 1
                candidate_id = int(candidate_half_id * s)


for k in invalid_id_list:
    invalid_id_sum += sum(invalid_id_list[k])
print(f"Output: {invalid_id_sum}")

