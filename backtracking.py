"""This module contains the sudoku solver using a recursive backtracking approach with no heuristics

Returns:
    int[][]: The solved sudoku puzzle 
"""
import random
import util
import test_puzzles

NODES_EXPANDED = 0

# backtracking by
def recursive_backtracking(assignment, variables):
    global NODES_EXPANDED
    if len(variables) == 0:
        return assignment

    row, col = util.select_unassigned_variable(variables)

    for value in order_domain_values():
        if is_consistent(assignment, row, col, value):
            assignment[row][col] = value
            variables.remove((row, col))
            NODES_EXPANDED += 1
            result = recursive_backtracking(assignment, variables)
            if result is not None:
                return result
            variables.append((row, col))
            assignment[row][col] = 0
    return None


# obtain all domain values
def order_domain_values():
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(values)
    return values


# consistency check
def is_consistent(assignment, row, col, value):
    # row check
    if value in assignment[row]:
        return False

    # col check
    for i in range(9):
        if assignment[i][col] == value:
            return False

    # box check
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if assignment[i][j] == value:
                return False
    return True

# run code
puzzle = test_puzzles.easy_puzzle

# Obtain cells that need to be filled
possible_variables = util.obtain_variables(puzzle)

util.print_sudoku(recursive_backtracking(puzzle, possible_variables))
print("Nodes expanded: " + str(NODES_EXPANDED))
