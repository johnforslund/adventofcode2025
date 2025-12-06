
##############################
##  Day 6: Trash Compactor  ##
##############################
# https://adventofcode.com/2025/day/6


##############
##  Part 1  ##
##############

# Imports
#import numpy as np
import os

# Initializing variables
#folder_path = os.path.dirname(os.path.abspath(__file__))   # TODO: Not working when running from REPL
folder_path = "day_6"
file_name = "input.txt"
sample_file_name = "input_sample.txt"
edgecase_file_name = "input_recreate_edgecase.txt"

with open(os.path.join(folder_path, file_name), "r") as f:
    document = f.read()

# Splitting document into fresh batches (first lines with ranges, then blank line, then lines with IDs)
document = document.split("\n")
symbols = document[-1]
problem_indices = []
problem_symbols = []
for i in range(len(symbols)):
    if symbols[i] in ["*", "+"]:
        problem_indices.append(i)
        problem_symbols.append(symbols[i])


# Checking input
print(f"Number of problems: {len(problem_symbols)}")
#print(f"Symbol indices: {problem_indices}")
print(f"Types of symbols: {set(problem_symbols)}")
print(f"Length of first row: {len(document[0])}")
print(f"Length of next to last row: {len(document[-2])}")
print(f"Length of symbol row: {len(document[-1])}")


# Parse document into individual problems
problems = []

# For Part 1:
for i in range(len(problem_indices)):
    problem = []
    for row in document[:-1]:
        if i == len(problem_indices) - 1:
            value = row[problem_indices[i]:]

        else:
            value = row[problem_indices[i]:problem_indices[i+1]]

        problem.append(int(value.strip()))
    problems.append(problem)


# For Part 2:
for i in range(len(problem_indices)):
    problem = []

    if i < len(problem_indices) - 1:
        problem_index_range = range(problem_indices[i], problem_indices[i+1] - 1)
    else:
        problem_index_range = range(problem_indices[i], len(document[0]))

    for j in problem_index_range:
        subvalues = []
        for row in document[:-1]:
            subvalues.append(row[j])
        value = int(''.join(x for x in subvalues))
        problem.append(value)    
    problems.append(problem)


total_sum = 0
for i in range(len(problems)):
    sum = 0
    for value in problems[i]:
        if problem_symbols[i] == '+':
            sum += value
        elif problem_symbols[i] == '*':
            if sum == 0:
                sum = value
            else:
                sum *= value
        else:
            print("Not a + or *")
    total_sum += sum
