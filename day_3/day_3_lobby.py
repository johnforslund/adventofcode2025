

####################
##  Day 3: Lobby  ##
####################
# https://adventofcode.com/2025/day/3


##############
##  Part 1  ##
##############

"""
# Reading sample file
with open("day_3/input_sample.txt", "r") as f:
    document = f.read().split()
"""

# Reading file
with open("day_3/input.txt", "r") as f:
    document = f.read().split()

# Checking input
print(f"Number of banks: {len(document)}")
print(f"Total number of batteries: {sum(len(b) for b in document)}")
print(f"Minimum bank length: {min(len(b) for b in document)}")
print(f"Maximum bank length: {max(len(b) for b in document)}")
print(f"Average bank length: {sum(len(b) for b in document) / len(document)}")
print(f"First 5 banks: {document[:5]}")

# Input consists of a series of banks of batteries.
# Each bank consists of a number of batteries in immutable order.
# Each battery consists of its joltage rating which is an integer between 1 and 9.

# You can turn on two batteries in every bank, from left to right.
# The total joltage of the bank is then the digit formed by those two batteries (e.g. first battery with joltage 3 and second battery with joltage 7 => bank's joltage is 37).

# Goal is to find the maximum joltage of every bank, and sum them all up.

def calculate_total_output_joltage(document: list[str]) -> int:
    total_output_joltage = 0

    # Loop through banks
    for bank in document:
        bank_joltage = calculate_max_bank_joltage(bank)
        total_output_joltage += bank_joltage

    return total_output_joltage


def calculate_max_bank_joltage(bank: str) -> int:

    # Find the first highest joltage battery
    first_battery_index, first_battery_joltage = get_highest_joltage_battery(bank, 0, len(bank) - 1)    # -1 to ensure at least one battery remains for second battery

    # Find the second highest joltage battery, starting from index after the first battery
    second_battery_index, second_battery_joltage = get_highest_joltage_battery(bank, first_battery_index + 1, len(bank))    # +1 to not include the first battery
    
    max_bank_joltage = int(str(first_battery_joltage) + str(second_battery_joltage))
    assert max_bank_joltage == int(bank[first_battery_index] + bank[second_battery_index]), "Max bank joltage calculation error!"   # Sanity check

    return max_bank_joltage


def get_highest_joltage_battery(bank: str, start_index: int, end_index: int) -> tuple[int, int]:
    """ Function to get highest joltage battery in a bank between start_index and end_index (inclusive) """
    for i in range(start_index, end_index):
        if i == start_index:
            candidate_max_battery = int(bank[i])    # Always set first battery as candidate max battery
            max_battery_index = i                   # Include index of first battery for sanity check & later use
        else:
            if int(bank[i]) > candidate_max_battery:
                candidate_max_battery = int(bank[i])
                max_battery_index = i
        
    max_joltage = candidate_max_battery
    
    return max_battery_index, max_joltage


output = calculate_total_output_joltage(document)

print(f"Output: {output}")



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

