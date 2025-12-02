

##############################
##  Day 1: Secret Entrance  ##
##############################
# https://adventofcode.com/2025/day/1



##############
##  Part 1  ##
##############

# Reading file
with open("day_1/input.txt", "r") as f:
    document = f.read().splitlines()

# Checking input
print(f"Number of rotations: {len(document)}")
print(f"Types of directions: {set([rotation[0] for rotation in document])}")
print(f"Min steps in a rotation: {min([int(rotation[1:]) for rotation in document])}")
print(f"Max steps in a rotation: {max([int(rotation[1:]) for rotation in document])}")
print(f"First 10 rotations: {document[:10]}")

# Input consists of a series of rotations [XY].
# X = "L" (left) or "R" (right).
# Y = positive integer starting from 1 to 999.


# Process is a dial that goes from 0 to 99, starts at 50, and turns left or right Y steps.
# Output is a positive integer, consisting of the number of times the dial reached 0 after every turn.

dial = 50  # Starting position of the dial
count_zeros = 0  # Count of times the dial reaches 0

for rotation in document:
    direction = rotation[0]    # "L" or "R"
    steps = int(rotation[1:])

    if direction == "L":
        dial = (dial - steps) % 100
    elif direction == "R":
        dial = (dial + steps) % 100

    if dial == 0:
        count_zeros += 1


print(f"Output: {count_zeros}")



##############
##  Part 2  ##
##############


dial = 50  # Starting position of the dial
full_turns = 0  # Count of full turns aka when crossing 0

for n in range(len(document)):
    print(f"Before rotation: dial={dial}, full_turns={full_turns}")

    rotation = document[n]
    print(f"Processing rotation nr {n}: {rotation}")

    direction = rotation[0]    # "L" or "R"
    steps = int(rotation[1:])

    if direction == "L":
        if dial == 0:
            dial = 100    # Adjust to handle exact 0 case, without it the integer division fails
        full_turns += abs((dial - steps) // 100)
        dial = (dial - steps) % 100
        if dial == 0:     # Adjusted to handle the dial landing exactly on 0, as without it the integer division misses this case
            full_turns += 1
    elif direction == "R":
        full_turns += (dial + steps) // 100
        dial = (dial + steps) % 100
    
    if n == len(document) - 1:
        if dial == 0:
            full_turns += 1  # Final check if last rotation ended exactly on 0


print(f"Output: {full_turns}")



