"""This module contains the sudoku solver using a recursive backtracking approach with a 
    forward checking heuristic

Returns:
    int[][]: The solved sudoku puzzle 
"""
import util
import test_puzzles

NODES_EXPANDED = 0


# backtracking by
def recursive_backtracking_fc(assignment, variables):
    """Recursive backtracking algorithm with forward checking

    Args:
        assignment (int[][]): current instance of the puzzle
        variables ([int,int][]): coordinates that still need a number

    Returns:
        _type_: _description_
    """
    global NODES_EXPANDED
    if len(variables) == 0:
        return assignment

    row, col = util.select_unassigned_variable(variables)
    values = order_domain_values(assignment, row, col)

    for value in values:
        if util.is_consistent(assignment, row, col, value):
            assignment[row][col] = value
            variables.remove((row, col))
            NODES_EXPANDED += 1
            result = recursive_backtracking_fc(assignment, variables)
            if result is not None:
                return result
            variables.append((row, col))
            assignment[row][col] = 0
    return None


# obtain all domain values
def order_domain_values(assignment, row, col):
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        if assignment[row][i] in values:
            values.remove(assignment[row][i])  # Remove values from the same row
        if assignment[i][col] in values:
            values.remove(assignment[i][col])  # Remove values from the same column

    box_row = 3 * (row // 3)
    box_col = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if assignment[box_row + i][box_col + j] in values:
                values.remove(
                    assignment[box_row + i][box_col + j]
                )  # Remove values from the same box

    return values


def forward_check(assignment, row, col):
    for i in range(9):
        if (
            i != col
            and assignment[row][i] == 0
            and not order_domain_values(assignment, row, i)
        ):
            return False
        if (
            i != row
            and assignment[i][col] == 0
            and not order_domain_values(assignment, i, col)
        ):
            return False

        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if (
                    (box_row + i != row or box_col + j != col)
                    and assignment[box_row + i][box_col + j] == 0
                    and not order_domain_values(assignment, box_row + i, box_col + j)
                ):
                    return False  # Empty cell in the same box has no valid values


# run code
puzzle = test_puzzles.easy_puzzle

possible_variables = util.obtain_variables(puzzle)

util.print_sudoku(recursive_backtracking_fc(puzzle, possible_variables))
print("Nodes expanded: " + str(NODES_EXPANDED))
