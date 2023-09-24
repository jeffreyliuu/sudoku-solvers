"""Util folder responsible of holding valuable utility functions to help the sudoku solver 
    algorithms.
"""
import random


def print_sudoku(puzzle):
    """Helper method to print the sudoku puzzle neatly in the console.

    Args:
        puzzle (int[][]): An instance of the sudoku puzzle
    """
    for i, row in enumerate(puzzle):
        for j, num in enumerate(row):
            print(num, end=" ")
            if (j + 1) % 3 == 0 and j < 8:
                print("|", end=" ")
        print()
        if (i + 1) % 3 == 0 and i < 8:
            print("-" * 21)


def obtain_variables(assignment):
    """Method that goes through a sudoku puzzle and figures which cells still need to be filled

    Args:
        assignment (int[][]): Instance of a sudoku puzzle that isn't solved yet

    Returns:
        ((int,int)[]): Array of cell coordinates that still need to be filled
    """
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if assignment[i][j] == 0:
                empty_cells.append((i, j))
    return empty_cells


def is_consistent(assignment, row, col, value):
    """Method that analyzes a sudoku puzzle and determines if it is still valid after placing
    value in (row, col)

    Args:
        assignment (int[][]): instance of the sudoku puzzle
        row (int): row of the cell we are obtaining domain values for
        col (int): column of the cell we are obtaining domain values for
        value (int): value is to be placed.

    Returns:
        boolean: Returns true if the sudoku puzzle is still valid after value is placed,
            and false otherwise.
    """
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


# select a random variable from possible variables left
def select_unassigned_variable(variables):
    """Method that randomly chooses a cell to be filled in. Only used in solo recursive
    backtracking and forward checking algorithms.

    Args:
        variables ((int,int)[]): Array of cell coordinates that still need to be filled

    Returns:
        (int,int): A cell coordinate that will be filled in next.
    """
    return random.choice(variables)

def get_domain(assignment, row, col):
    """Part of the forward checking aspect of the algorithm where we determine in advance the 
        possible values that a cell can take to decrease the amount of lookups.

    Args:
        assignment (int[][]): instance of the sudoku puzzle
        row (int): row of the cell we are obtaining domain values for
        col (int): column of the cell we are obtaining domain values for

    Returns:
        int[]: array that contains the possible values that the cell (row, col) can take
    """
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
