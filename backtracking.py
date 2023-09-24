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
    """Normal recursive backtracking algorithm to find a consistent assignment for the sudoku 
        problem.

    Args:
        assignment (int[][]): instance of the sudoku problem
        variables ([int,int][]): array of coordinates that still need a value placed

    Returns:
        int[][]: Solution to the sudoku puzzle
    """
    global NODES_EXPANDED
    if len(variables) == 0:
        return assignment

    row, col = util.select_unassigned_variable(variables)

    for value in order_domain_values():
        if util.is_consistent(assignment, row, col, value):
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
    """Determine the order of possible values that the cell can take. In this algorithm, 
        they are randomly generated.

    Returns:
        int[]: array of values that can fill a cell
    """
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(values)
    return values

if __name__ == "__main__":
    puzzle = test_puzzles.easy_puzzle
    possible_variables = util.obtain_variables(puzzle)
    solved_puzzle = recursive_backtracking(puzzle, possible_variables)

    util.print_sudoku(solved_puzzle)
    print(f"Nodes expanded: {NODES_EXPANDED}")
