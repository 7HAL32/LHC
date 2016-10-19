from operator import mul
from fractions import Fraction
from functools import reduce


def nck(n, k):
    """
    Calculates the binomial coefficient aka "n choose k

    :param n: int
    :param k: int (>= 0)
    :raises ValueError: k is negative
    :raises TypeError: n, k are no integers
    :return: int
    """
    if k < 0:
        raise ValueError('k has to be a non-negative integer')
    return int(reduce(mul, (Fraction(n - i, i + 1) for i in range(k)), 1))
