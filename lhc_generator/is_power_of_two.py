"""
Handcrafted with :heart: by Lutz Thies in 2016.
"""


def is_power_of_two(number):
    """
    Checks if a number is a power of two

    :param number: int
    :return: bool
    """
    # powers of two should always be positive integers
    if type(number) is not int or number < 1:
        return False
    # if a number is a power of two, the bitwise AND with it's predecessor has to be zero
    return (number & (number - 1)) == 0
