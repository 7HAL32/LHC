def is_power_of_two(number):
    """
    Check if number is a power of two
    :param number: int
    :return: bool
    """
    # powers of two should always be positive integers
    if type(number) != int or number < 1:
        return False
    # if number was a power the bitwise AND with it's bit the predecessor has to be zero
    return (number & (number - 1)) == 0
