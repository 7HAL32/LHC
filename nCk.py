from operator import mul
from fractions import Fraction
from functools import reduce

def nCk(n, k):
    """ Calculates the binomial coefficient aka "n choose k"

        :raises ValueError:
            If k is negative
        :raises TypeError:
            If n, k are no integers
        :returns:
            An integer
    """
    if k < 0:
        raise ValueError('k has to be a non-negative integer')
    return int(reduce(mul, (Fraction(n - i, i + 1) for i in range(k)), 1))
