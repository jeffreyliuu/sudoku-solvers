"""This module contains the sudoku solver algorithm with recursive backtracking, forward checking,
    and heuristics

Returns:
    int[][]: the solved sudoku puzzle
"""

import time
import test_puzzles
import util

NODES_EXPANDED = 0

def recursive_backtracking_fc_h(assignment, variables):
    """Recursive backtracking algorithm with forward checking and heuristics.

    Args:
        assignment (int[][]): instance of the sudoku problem
        variables ([int,int][]): array of coordinates that still need a value placed

    Returns:
        int[][]: Solution to the sudoku puzzle
    """
    global NODES_EXPANDED
    if len(variables) == 0:
        return assignment

    row, col = select_unassigned_variable(assignment, variables)
    domain = util.get_domain(assignment, row, col)

    values = order_domain_values(assignment, row, col, domain)

    for value in values:
        if util.is_consistent(assignment, row, col, value):
            assignment[row][col] = value
            variables.remove((row, col))
            if forward_check(assignment, row, col):
                NODES_EXPANDED += 1
                result = recursive_backtracking_fc_h(assignment, variables)
                if result is not None:
                    return result
            variables.append((row, col))
            assignment[row][col] = 0
    return None


def select_unassigned_variable(assignment, variables):
    """To determine which variable we should assign, we use the Least Constrained 
    Value heuristic. That is, which coordinates have the least number of possible assigned
    values.

    Args:
        assignment (int[][]): instance of the sudoku problem
        variables ([int,int][]): array of coordinates that still need a value placed

    Returns:
        _type_: _description_
    """
    return min(
        variables,
        key=lambda variable: len(util.get_domain(assignment, variable[0], variable[1])),
    )


# obtain lcv domain values
def order_domain_values(assignment, row, col, domain):
    # helper to help sort values by least constraining value
    def least_constrained_value(value):
        count = 0

        for i in range(9):
            if (
                i != col
                and assignment[row][i] == 0
                and value in util.get_domain(assignment, row, i)
            ):
                count += 1
            if (
                i != row
                and assignment[i][col] == 0
                and value in util.get_domain(assignment, i, col)
            ):
                count += 1

        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if (
                    (box_row + i != row or box_col + j != col)
                    and assignment[box_row + i][box_col + j] == 0
                    and value in util.get_domain(assignment, box_row + i, box_col + j)
                ):
                    count += 1

        return count

    return sorted(domain, key=least_constrained_value)


def forward_check(assignment, row, col):
    # check same col/row if any empty values
    for i in range(9):
        if i != col and assignment[row][i] == 0 and not util.get_domain(assignment, row, i):
            return False
        if i != row and assignment[i][col] == 0 and not util.get_domain(assignment, i, col):
            return False

        # check same box
        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if (
                    (box_row + i != row or box_col + j != col)
                    and assignment[box_row + i][box_col + j] == 0
                    and not util.get_domain(assignment, box_row + i, box_col + j)
                ):
                    return False
        return True

if __name__ == "__main__":
    puzzle = test_puzzles.medium_puzzle

    possible_variables = util.obtain_variables(puzzle)
    start_time = time.time()
    util.print_sudoku(recursive_backtracking_fc_h(puzzle, possible_variables))
    print(f"--- {time.time() - start_time} seconds ---")
    print("Nodes expanded: " + str(NODES_EXPANDED))
