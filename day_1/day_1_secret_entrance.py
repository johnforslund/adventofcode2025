

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



