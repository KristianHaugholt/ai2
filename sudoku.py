# Sudoku problems.
# The CSP.ac_3() and CSP.backtrack() methods need to be implemented

from csp import CSP, alldiff


def print_solution(solution):
    """
    Convert the representation of a Sudoku solution, as returned from
    the method CSP.backtracking_search(), into a Sudoku board.
    """
    for row in range(width):
        for col in range(width):
            print(solution[f'X{row+1}{col+1}'], end=" ")
            if col == 2 or col == 5:
                print('|', end=" ")
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')


# Choose Sudoku problem
width = 9
box_width = 3

def run_on_file(path: str):
    grid = open(path).read().split()

    domains = {}
    for row in range(width):
        for col in range(width):
            if grid[row][col] == '0':
                domains[f'X{row+1}{col+1}'] = set(range(1, 10))
            else:
                domains[f'X{row+1}{col+1}'] = {int(grid[row][col])}

    edges = []
    for row in range(width):
        edges += alldiff([f'X{row+1}{col+1}' for col in range(width)])
    for col in range(width):
        edges += alldiff([f'X{row+1}{col+1}' for row in range(width)])
    for box_row in range(box_width):
        for box_col in range(box_width):
            edges += alldiff(
                [
                    f'X{row+1}{col+1}' for row in range(box_row * box_width, (box_row + 1) * box_width)
                    for col in range(box_col * box_width, (box_col + 1) * box_width)
                ]
            )

    csp = CSP(
        variables=[f'X{row+1}{col+1}' for row in range(width) for col in range(width)],
        domains={k: set(v) for k, v in domains.items()},
        edges=edges,
    )

    from time import perf_counter
    from pprint import pprint

    t0 = perf_counter()
    ac3_ok = csp.ac_3()
    t_ac3 = perf_counter() - t0

    # copy domains after AC-3
    domains_after_ac3 = {v: sorted(list(d)) for v, d in csp.domains.items()}

    t1 = perf_counter()
    solution = csp.backtracking_search()
    t_back = perf_counter() - t1

    total = perf_counter() - t0

    print('File:', path)
    print('AC-3 returned:', ac3_ok)
    print('AC-3 time (s):', t_ac3)
    print('Domains after AC-3:')
    pprint(domains_after_ac3)
    print('Backtracking calls:', csp.bt_calls)
    print('Backtracking failures:', csp.bt_failures)
    print('Backtracking time (s):', t_back)
    print('Total time (s):', total)
    print('Solution:')
    if solution:
        print_solution(solution)
    else:
        print('No solution')
    print('\n' + '='*60 + '\n')


if __name__ == '__main__':
    for fname in ['sudoku_easy.txt', 'sudoku_medium.txt', 'sudoku_hard.txt', 'sudoku_very_hard.txt']:
        run_on_file(fname)

# Expected output after implementing csp.ac_3() and csp.backtracking_search():
# True
# 7 8 4 | 9 3 2 | 1 5 6
# 6 1 9 | 4 8 5 | 3 2 7
# 2 3 5 | 1 7 6 | 4 8 9
# ------+-------+------
# 5 7 8 | 2 6 1 | 9 3 4
# 3 4 1 | 8 9 7 | 5 6 2
# 9 2 6 | 5 4 3 | 8 7 1
# ------+-------+------
# 4 5 3 | 7 2 9 | 6 1 8
# 8 6 2 | 3 1 4 | 7 9 5
# 1 9 7 | 6 5 8 | 2 4 3
