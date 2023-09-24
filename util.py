import random


def print_sudoku(puzzle):
    for i, row in enumerate(puzzle):
        for j, num in enumerate(row):
            print(num, end=" ")
            if (j + 1) % 3 == 0 and j < 8:
                print("|", end=" ")
        print()
        if (i + 1) % 3 == 0 and i < 8:
            print("-" * 21)


def obtain_variables(assignment):
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if assignment[i][j] == 0:
                empty_cells.append((i, j))
    return empty_cells


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


# select a random variable from possible variables left
def select_unassigned_variable(variables):
    return random.choice(variables)
