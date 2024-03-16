import numpy as np


def standard_basis_vector(size: int, index: int) -> np.ndarray:
    """Return the index-th standard basis vector with dimension size.

    >>> standard_basis_vector(2, 0).astype(int)
    array([1, 0])

    >>> standard_basis_vector(3, 0).shape
    (3,)

    >>> standard_basis_vector(4, 1).astype(int)
    array([0, 1, 0, 0])
    """
    return np.array([1 if i == index else 0 for i in range(size)])


def generate_transition_matrix(
    birth_rate: float, prob_survival: np.ndarray
) -> np.ndarray:
    """Return the transition matrix for given birth rate and probabilities of survival.

    >>> A = generate_transition_matrix(0.5, np.array([]))
    >>> np.isclose(A, np.array([[0.5]])).all()
    True

    >>> A = generate_transition_matrix(0.5, np.array([0.9]))
    >>> np.isclose(A, np.array([[0.5, 0.5], [0.9, 0.]])).all()
    True

    >>> generate_transition_matrix(1, np.array([1, 2, 3, 4]))
    array([[1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0],
           [0, 2, 0, 0, 0],
           [0, 0, 3, 0, 0],
           [0, 0, 0, 4, 0]])
    """
    l = len(prob_survival)+1
    return np.array([[birth_rate for i in range(l)] if j == 0 else [prob_survival[j-1] if i == j-1 else 0 for i in range(l)] for j in range(l)])
    pass


def transition_matrix_from_data(
    pop_year1: np.ndarray, pop_year2: np.ndarray
) -> np.ndarray:
    """Return the transition matrix for population data of to consecutive time steps.

    >>> A = transition_matrix_from_data(np.array([10, 0]), np.array([5, 9]))
    >>> np.isclose(A, np.array([[0.5, 0.5], [0.9, 0.]])).all()
    True

    >>> A = transition_matrix_from_data(np.array([10, 0, 0, 0, 0]), np.array([1, 9, 0, 0, 0]))
    >>> np.isclose(A, np.array([[0.1, 0.1, 0.1, 0.1, 0.1], [0.9, 0. , 0. , 0. , 0. ], [0. , 1. , 0. , 0. , 0. ], [0. , 0. , 1. , 0. , 0. ], [0. , 0. , 0. , 1. , 0. ]])).all()
    True

    """
    survival = [pop_year2[i] / pop_year1[i-1] if pop_year1[i-1] != 0 else 1 for i in range(1,len(pop_year1))]
    sum_thing = 0
    for i in pop_year1:
        sum_thing += i
    return generate_transition_matrix(pop_year2[0]/sum_thing, survival)


def advance_years(
    population: np.ndarray,
    years: int,
    birth_rate: float,
    prob_survival: np.ndarray,
) -> np.ndarray:
    """Compute the population after several years.

    >>> pop = advance_years(np.array([100, 0]), 0, 0.5, np.array([0.5]))
    >>> np.isclose(pop, np.array([100.,   0.])).all()
    True

    >>> pop = advance_years(np.array([100, 0]), 5, 0.5, np.array([0.5]))
    >>> np.isclose(pop, np.array([25.   , 15.625])).all()
    True

    >>> pop = advance_years(np.array([10, 0, 0, 0, 0]), 1, 0.1, np.array([0.9, 0.8, 0.7, 0.6]))
    >>> np.isclose(pop, np.array([1., 9., 0., 0., 0.])).all()
    True

    >>> pop = advance_years(np.array([10, 0, 0, 0, 0]), 2, 0.1, np.array([0.9, 0.8, 0.7, 0.6]))
    >>> np.isclose(pop, np.array([1. , 0.9, 7.2, 0. , 0. ])).all()
    True

    """
    mat = generate_transition_matrix(birth_rate, prob_survival)
    vec = population
    for i in range(years):
        vec = np.matmul(mat,vec)
    return vec
    pass


def years_until_extinct(
    population: np.ndarray,
    birth_rate: float,
    prob_survival: np.ndarray,
    max_years: int = 1000,
) -> int:
    """Compute number of years until the population is extinct.

    >>> pop = np.array([100, 0])
    >>> years_until_extinct(pop, 0.5, np.array([0.5]))
    21
    >>> (pop == np.array([100, 0])).all()
    True

    >>> years_until_extinct(np.array([10, 0, 0, 0, 0]), 0.1, np.array([0.9, 0.8, 0.7, 0.6]))
    5

    >>> years_until_extinct(np.array([0.1, 0.2, 0.4, 0.2]), 0.8, 0.9 * np.ones((3,)))
    0

    >>> years_until_extinct(np.array([1000, 0]), 0.6, np.array([0.7]), 10)
    Traceback (most recent call last):
    ...
    ValueError: Population lives more than 10 years.
    """
    mat = generate_transition_matrix(birth_rate, prob_survival)
    vec = population
    work = True
    for j in vec:
        if j >= 1:
            work = False
    if work:
        return 0
    for i in range(max_years):
        vec = np.matmul(mat,vec)
        work = True
        for j in vec:
            if j >= 1:
                work = False
        if work:
            return i+1
    raise ValueError(f"Population lives more than {max_years} years.")


def reach_age_with_prob(p: float, prob_survival: np.ndarray) -> int:
    """Return the largest age which is reached with probability p.

    >>> reach_age_with_prob(0.8, np.array([]))
    0

    >>> reach_age_with_prob(0.8, np.array([0.5, 0.8, 0.7]))
    0

    >>> reach_age_with_prob(0.4, np.array([0.5, 0.8, 0.7]))
    1

    >>> reach_age_with_prob(0.3, np.array([0.5, 0.8, 0.7]))
    2

    >>> reach_age_with_prob(0.1, np.array([0.5, 0.8, 0.7]))
    3
    """
    prod = [1 for i in range(len(prob_survival)+2)]
    for i in range(1,len(prob_survival)+1):
        prod[i] = prod[i-1]*prob_survival[i-1]
    prod[-1]=0
    for i in range(len(prod)):
        if prod[i] >= p and prod[i+1] < p:
            return i
    return -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
