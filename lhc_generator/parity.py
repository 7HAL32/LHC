"""
Handcrafted with :heart: by Lutz Thies in 2016.
"""

from functools import reduce


def parity(bits):
    """
    Calculates the parity of a bit sequence

    :param bits: list of ints
    :returns: int
    """
    return reduce(lambda x, y: x ^ y, bits)
