"""This module contains the sudoku solver using a recursive backtracking approach with 
    forward checking

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
        int[][]: Solution to the sudoku puzzle
    """
    global NODES_EXPANDED
    if len(variables) == 0:
        return assignment

    row, col = util.select_unassigned_variable(variables)
    values = util.order_domain_values(assignment, row, col)

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



def forward_check(assignment, row, col):
    """Forward checking aspect of the algorithm where we stop recursing if we have no more
        values that a cell can take and the assignment is still not complete.

    Args:
        assignment (int[][]): instance of the sudoku puzzle
        row (int): row of the cell we are obtaining domain values for
        col (int): column of the cell we are obtaining domain values for

    Returns:
        bool: boolean that returns true if the current cell still has possible values, 
            and false otherwise
    """
    for i in range(9):
        if (
            i != col
            and assignment[row][i] == 0
            and not util.order_domain_values(assignment, row, i)
        ):
            return False
        if (
            i != row
            and assignment[i][col] == 0
            and not util.order_domain_values(assignment, i, col)
        ):
            return False

        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if (
                    (box_row + i != row or box_col + j != col)
                    and assignment[box_row + i][box_col + j] == 0
                    and not util.order_domain_values(assignment, box_row + i, box_col + j)
                ):
                    return False  # Empty cell in the same box has no valid values


if __name__ == "__main__":
    puzzle = test_puzzles.medium_puzzle
    possible_variables = util.obtain_variables(puzzle)
    solved_puzzle = recursive_backtracking_fc(puzzle, possible_variables)

    util.print_sudoku(solved_puzzle)
    print(f"Nodes expanded: {NODES_EXPANDED}")
