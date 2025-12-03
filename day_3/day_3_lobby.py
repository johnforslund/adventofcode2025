

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

""" TODO: LEGACY
def calculate_total_output_joltage(document: list[str]) -> int:
    total_output_joltage = 0

    # Loop through banks
    for bank in document:
        bank_joltage = calculate_max_bank_joltage(bank)
        total_output_joltage += bank_joltage

    return total_output_joltage
"""

""" TODO: LEGACY
def calculate_max_bank_joltage(bank: str) -> int:

    # Find the first highest joltage battery
    first_battery_index, first_battery_joltage = get_highest_joltage_battery(bank, 0, len(bank) - 1)    # -1 to ensure at least one battery remains for second battery

    # Find the second highest joltage battery, starting from index after the first battery
    second_battery_index, second_battery_joltage = get_highest_joltage_battery(bank, first_battery_index + 1, len(bank))    # +1 to not include the first battery
    
    max_bank_joltage = int(str(first_battery_joltage) + str(second_battery_joltage))
    assert max_bank_joltage == int(bank[first_battery_index] + bank[second_battery_index]), "Max bank joltage calculation error!"   # Sanity check

    return max_bank_joltage
"""

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



##############
##  Part 2  ##
##############


# Change: You can now turn on 12 batteries in every bank, from left to right.
# So, instead of 2 batteries, it is now 12 batteries. Nothing else changed.

# Let's make the functions more general to handle any number of batteries to turn on:
def calculate_max_bank_joltage(bank: str, num_batteries: int) -> int:

    # Initialize list to hold selected batteries' indices and joltages
    battery_indices = []
    battery_joltages = []

    # Loop through all the batteries to turn on
    for b in range(num_batteries):
        battery_index, battery_joltage = get_highest_joltage_battery(bank, 0 if b == 0 else battery_indices[-1] + 1, len(bank) - (num_batteries - b - 1))
        battery_indices.append(battery_index)
        battery_joltages.append(battery_joltage)
        
    max_bank_joltage = int(''.join(str(j) for j in battery_joltages))
    assert max_bank_joltage == int(''.join(bank[i] for i in battery_indices)), "Max bank joltage calculation error!"   # Sanity check

    return max_bank_joltage


# And add the new parameter num_batteries when calling the main function:
def calculate_total_output_joltage(document: list[str], num_batteries: int) -> int:
    total_output_joltage = 0

    # Loop through banks
    for bank in document:
        bank_joltage = calculate_max_bank_joltage(bank, num_batteries)
        total_output_joltage += bank_joltage

    return total_output_joltage


output = calculate_total_output_joltage(document, 12)  # Now specifying number of batteries to turn on
print(f"Output: {output}")