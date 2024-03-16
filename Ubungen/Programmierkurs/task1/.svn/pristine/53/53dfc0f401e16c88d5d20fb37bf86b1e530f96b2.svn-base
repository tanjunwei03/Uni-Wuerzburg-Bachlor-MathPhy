"""This module provides means of working with permutations.

In particular, algebraic operations are provided along with the
means to apply them to lists.
"""

from typing import Callable
import itertools

Permutation = tuple[int]


def is_permutation(tpl: tuple[int]) -> bool:
    """Determine whether `tpl` defines a valid permutation.

    >>> is_permutation((0, 3, 1, 2))
    True

    >>> is_permutation((4, 1, 2))
    False

    >>> is_permutation(tuple("string"))
    False
    """
    s = set(tpl)
    if s != set(range(len(tpl))):
        return False
    count = {i:False for i in tpl}
    for i in tpl:
        if count[i] == True:
            return False
    return True
    pass


def composite(a: Permutation, b: Permutation) -> Permutation:
    """Form the composite of two permutations.

    >>> sigma = (0, 2, 1) # Swap second and third element
    >>> composite(sigma, sigma)  # Swapping twice yields the identity
    (0, 1, 2)

    >>> composite((3, 2, 4, 0, 1), (4, 0, 1, 3, 2))
    (1, 3, 2, 0, 4)
    """
    if len(a) != len(b):
        raise ValueError(
            f"permutations of unequal length ({len(a)} "
            f"and {len(b)}) cannot be composed"
        )
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(perm: Permutation) -> Permutation:
    """Determine the inverse of a given permutation.

    # Self-inverse
    >>> inverse((0, 2, 1))
    (0, 2, 1)

    >>> inverse((2, 0, 1))
    (1, 2, 0)

    # Cycle-right inverted by cycle-left
    >>> inverse((3, 0, 1, 2))
    (1, 2, 3, 0)
    """
    out = [0 for i in perm]
    for i in range(len(perm)):
        out[perm[i]] = i
    return tuple(out)
        

def apply(perm: Permutation, x: tuple) -> tuple:
    """Transform a given tuple with a permutation.

    # Does nothing
    >>> apply((0, 1, 2), ("foo", "bar", "baz"))
    ('foo', 'bar', 'baz')

    # Reverses
    >>> apply((1, 0), ("a", "b"))
    ('b', 'a')

    >>> apply((0, 2, 1), ("a", "b", "c"))
    ('a', 'c', 'b')
    """
    if len(perm) != len(x):
        raise ValueError(
            f"a permutation of length {len(perm)} cannot be "
            f"applied to a list of length {len(x)}"
        )
    return tuple(x[i] for i in perm)


def as_function(perm: Permutation) -> Callable:
    """Create a function which represents a given permutation.

    >>> sigma = as_function((0, 3, 1, 2))
    >>> sigma(("a", "b", "c", "d"))
    ('a', 'd', 'b', 'c')

    >>> perm = (3, 2, 1, 0)
    >>> arg = (3, 0, 1, 2)
    >>> as_function(perm)(arg) == apply(perm, arg)
    True

    # Identity permutation
    >>> n = 8
    >>> rho = as_function(tuple(range(n)))
    >>> x = tuple(range(n))
    >>> rho(x) == x
    True
    """
    return lambda x : apply(perm,x)


def num_fixed_points(perm: Permutation) -> int:
    """Determine the number of fixed points.

    # All points fixed
    >>> num_fixed_points((0, 1, 2))
    3

    # No fixed points (i.e., the permutation is a "derangement")
    >>> num_fixed_points((2, 0, 1))
    0

    >>> num_fixed_points((3, 1, 2, 0))
    2
    """
    count = 0
    for i in range(len(perm)):
        if perm[i] == i:
            count += 1

    return count


def permutations_with_fixed_points(length: int, num_fixed: int) -> list[Permutation]:
    """Find all permutations of a given length and number of fixed points.

    NOTE: In the following examples, the output is sorted to make it
    order-independent because no specific ordering is demanded as part
    of this task.

    # Derangements of length 3.
    >>> sorted(permutations_with_fixed_points(3, 0))
    [(1, 2, 0), (2, 0, 1)]

    # Impossible: 4 fixed points at length 2.
    >>> permutations_with_fixed_points(2, 4)
    []

    # Also impossible: only 3 fixed points at length 4.
    >>> permutations_with_fixed_points(4, 3)
    []

    >>> sorted(permutations_with_fixed_points(4, 2))
    [(0, 1, 3, 2), (0, 2, 1, 3), (0, 3, 2, 1), (1, 0, 2, 3), (2, 1, 0, 3), (3, 1, 2, 0)]
    """
    lst = []
    perms = list(itertools.permutations(range(length)))
    for perm in perms:
        if num_fixed_points(perm) == num_fixed:
            lst.append(perm)
    return lst


if __name__ == "__main__":
    import doctest

    doctest.testmod()
