import time
import test_puzzles
import util

NODES_EXPANDED = 0


def recursive_backtracking_fc_h(assignment, variables):
    global NODES_EXPANDED
    if len(variables) == 0:
        return assignment

    row, col = select_unassigned_variable(assignment, variables)
    domain = get_domain(assignment, row, col)

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


# select a random variable from possible variables left
def select_unassigned_variable(assignment, variables):
    return min(
        variables,
        key=lambda variable: len(get_domain(assignment, variable[0], variable[1])),
    )


# get domain
def get_domain(assignment, row, col):
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        if assignment[row][i] in values:
            values.remove(assignment[row][i])
        if assignment[i][col] in values:
            values.remove(assignment[i][col])

    box_row = 3 * (row // 3)
    box_col = 3 * (col // 3)
    for x in range(3):
        for y in range(3):
            if assignment[box_row + x][box_col + y] in values:
                values.remove(assignment[box_row + x][box_col + y])
    return values


# obtain lcv domain values
def order_domain_values(assignment, row, col, domain):
    # helper to help sort values by least constraining value
    def least_constrained_value(value):
        count = 0

        for i in range(9):
            if (
                i != col
                and assignment[row][i] == 0
                and value in get_domain(assignment, row, i)
            ):
                count += 1
            if (
                i != row
                and assignment[i][col] == 0
                and value in get_domain(assignment, i, col)
            ):
                count += 1

        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if (
                    (box_row + i != row or box_col + j != col)
                    and assignment[box_row + i][box_col + j] == 0
                    and value in get_domain(assignment, box_row + i, box_col + j)
                ):
                    count += 1

        return count

    return sorted(domain, key=least_constrained_value)


def forward_check(assignment, row, col):
    # check same col/row if any empty values
    for i in range(9):
        if i != col and assignment[row][i] == 0 and not get_domain(assignment, row, i):
            return False
        if i != row and assignment[i][col] == 0 and not get_domain(assignment, i, col):
            return False

        # check same box
        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if (
                    (box_row + i != row or box_col + j != col)
                    and assignment[box_row + i][box_col + j] == 0
                    and not get_domain(assignment, box_row + i, box_col + j)
                ):
                    return False
        return True


# run code
puzzle = test_puzzles.easy_puzzle

possible_variables = util.obtain_variables(puzzle)
start_time = time.time()
util.print_sudoku(recursive_backtracking_fc_h(puzzle, possible_variables))
print("--- %s seconds ---" % (time.time() - start_time))
print("Nodes expanded: " + str(NODES_EXPANDED))
