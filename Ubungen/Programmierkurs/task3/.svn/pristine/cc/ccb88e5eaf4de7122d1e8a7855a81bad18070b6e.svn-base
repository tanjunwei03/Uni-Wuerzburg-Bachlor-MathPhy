import sys

import numpy as np

# Assumptions: two-dimensional, square shape, side length is a square number,
# entries are nonnegative integers, zero represents a missing value.
Puzzle = np.array


def base(p: Puzzle) -> int:
    """Determine the base of a puzzle, e.g., 3 for a size 9 x 9 puzzle.

    >>> base(np.zeros((9, 9)))
    3

    >>> sudoku = np.array([[1, 2, 0, 3], [0, 3, 2, 1], [2, 1, 3, 0], [3, 0, 1, 2]])
    >>> base(sudoku)
    2
    """
    return int(np.sqrt(len(p)))


def copy_puzzle(p: Puzzle) -> Puzzle:
    """Return a fully independent copy of a puzzle.

    >>> a = np.array([[1, 2, 0, 3], [0, 3, 2, 1], [2, 1, 3, 0], [3, 0, 1, 2]])
    >>> b = copy_puzzle(a)
    >>> b[0, 2] = 4
    >>> np.array_equal(a, b)
    False
    """
    return np.copy(p)


def from_file(path: str) -> Puzzle:
    """Read a puzzle from the file at path.

    The input is assumed to be lines of numbers or underscores separated by
    whitespace. Underscores represent missing values.

    # Not an actual test, just for illustration
    >>> with open('puzzles/example_4x4_puzzle.txt') as f:
    ...     print(f.read().strip())
    1 2 _ 3
    _ 3 2 1
    2 1 3 _
    3 _ 1 2

    >>> sudoku = from_file('puzzles/example_4x4_puzzle.txt')
    >>> ref = [[1, 2, 0, 3], [0, 3, 2, 1], [2, 1, 3, 0], [3, 0, 1, 2]]
    >>> (sudoku == np.array(ref)).all()
    True
    >>> sudoku.dtype
    dtype('int64')
    """
    f = open(path).read().strip()
    arr = [[]]
    word = ""
    for i in f:
        if i == " " or i == "\n":
            if word == "_":
                arr[-1].append(0)
            else:
                arr[-1].append(int(word))
            word = ""
        else:
            word += i
        if i == "\n":
            arr.append([])
    arr[-1].append(int(word))
    return np.array(arr,dtype=np.int64)


def as_string(p: Puzzle) -> str:
    """Format a Sudoku puzzle as a string.

    The resulting string has one line per row and entries separated by a
    single space. Empty squares are marked with an underscore and non-empty
    squares are represented as numbers.

    >>> s = np.zeros((4, 4), dtype=int)
    >>> s[1, 1] = 2
    >>> print(as_string(s))
    _ _ _ _
    _ 2 _ _
    _ _ _ _
    _ _ _ _
    """
    return "\n".join(map(lambda x : " ".join(map(lambda y:"_" if y == 0 else str(y),x)),p))


def in_row(i: int, p: Puzzle) -> set[int]:
    """Return the entries in row i (0-indexed) as a set.

    >>> sudoku = np.array([[1, 2, 3, 4], [3, 0, 2, 0], [4, 0, 0, 0], [0, 1, 0, 0]])
    >>> sorted(in_row(1, sudoku))
    [2, 3]
    >>> sorted(in_row(2, sudoku))
    [4]
    """
    s=set(p[i])
    if 0 in s:
        s.remove(0)
    return s


def in_column(j: int, p: Puzzle) -> set[int]:
    """Return the entries in column j (0-indexed) as a set.

    >>> sudoku = np.array([[1, 2, 3, 4], [3, 0, 2, 0], [4, 0, 0, 0], [0, 1, 0, 0]])
    >>> sorted(in_column(0, sudoku))
    [1, 3, 4]
    >>> sorted(in_column(2, sudoku))
    [2, 3]
    """
    s = {i[j] for i in p}
    if 0 in s:
        s.remove(0)
    return s


def in_block(i: int, j: int, p: Puzzle) -> set[int]:
    """Return the entries in the block at row i and column j as a set.

    For a Sudoku with base n, the block will have size n x n.

    # Base 2 example, containing 4 blocks of size 2 x 2.
    >>> sudoku = np.array([[1, 2, 3, 4], [3, 0, 2, 0], [4, 0, 0, 0], [0, 1, 0, 0]])
    >>> sorted(in_block(3, 2, sudoku)) # Block around (3, 2), lower right quadrant
    []
    >>> sorted(in_block(1, 1, sudoku)) # Upper left quadrant
    [1, 2, 3]
    """
    size = base(p)
    row = i // size
    column = j // size
    s = set()
    for i in range(row*size,(row+1)*size):
        for j in range(column*size,(column+1)*size):
            s.add(p[i][j])
    if 0 in s:
        s.remove(0)
    return s


def isSolution(p: Puzzle):
    """Generate all solutions for the given puzzle.
    >>> sudoku = from_file('puzzles/example_4x4_solution.txt')
    >>> isSolution(sudoku)
    True
"""
    isSol = True
    l = len(p)
    size = base(p)
    checkAgainst = set(range(1,l+1))
    for i in range(l):
        if in_row(i,p) != checkAgainst:
            isSol = False
            break
    if isSol:
        for i in range(l):
            if in_column(i,p) != checkAgainst:
                isSol = False
                break
    if isSol:
        for i in range(0,l,size):
            for j in range(0,l,size):
                if in_block(i,j,p) != checkAgainst:
                    isSol = False
                    break
    return isSol
    
def solve(p: Puzzle):
    """Generate all solutions for the given puzzle.
    >>> sudoku = from_file('puzzles/example_9x9_puzzle.txt')
    >>> solve(sudoku)
"""
    #check if we have a solution
    l = len(p)
    size = base(p)
    checkAgainst = set(range(1,l+1))

    if isSolution(p):
        return [p]

    #go to the next nonzero element
    row = 0
    column = 0
    breaking = False
    for i in range(l):
        if breaking:
            break
        for j in range(l):
            if p[i][j] == 0:
                breaking = True
                row,column = i,j
                break

    #what are the non allowed elements
    nonAllowed = in_row(row,p).union(in_column(column,p)).union(in_block(row,column,p))
    allowed = [i for i in checkAgainst if i not in nonAllowed]
    lst = []
    for i in allowed:
        pcopy = copy_puzzle(p)
        pcopy[row][column] = i
        lst += solve(pcopy)
    return lst


if __name__ == "__main__":
    if len(sys.argv) < 2:
        import doctest

        doctest.testmod()
    else:
        sudoku = from_file(sys.argv[1])
        for solution in solve(sudoku):
            print()
            print(as_string(solution))
