"""
Package: 7HAL32/lhc_generator

Functions to calculate necessary parameters for the construction of channel codes (e.g. linear Hamming codes).

Handcrafted with :heart: by Lutz Thies in 2016.
"""

import math
from .nck import nck


def needed_redundancy(ec, n):
    """
    Calculates the minimum number of redundant bits k_min
    (for more information have a look at /docs/redundancy.pdf)

    :param ec: int (targeted error correction capability)
    :param n: int (overall code word length)
    :returns: int (minimum of redundant digits k_min)
    """
    k = sum([nck(n, x) for x in range(0, ec + 1)])
    # smallest indivisible unit is a bit
    k_min = math.ceil(math.log(k, 2))
    return k_min


def construct_code(l, ec):
    """
    Constructs a minimal code signature meeting the given requirements

    :param l: int (length of source alphabet words)
    :param ec: int (number of errors that will be correctable)
    :raises ValueError: l <= 1, ec < 0
    :raises TypeError: l, ec are no integers
    :returns: n, l, k (code signature, where:   n channel word length,
                                                l source alphabet word length,
                                                k number of redundant digits)
    """
    message = "watch out and think about, what you were trying to do here"
    if l < 1 or ec < 0:
        raise(ValueError, message)
    if type(l) != int or type(ec) != int:
        raise(ValueError, message)

    n = l
    while n - needed_redundancy(ec, n) != l:
        n += 1
    return n, l, n - l
