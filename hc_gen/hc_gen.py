import math
import numpy as np
from .nck import nck


def needed_redundancy(i, k, n):
    """

    :param i: int
    :param k: int
    :param n: int
    :return: int
    """
    summed = 0
    for x in range(i, k + 1):
        summed += nck(n, x)
    return math.ceil(math.log(summed, 2))


def calc_code(l, ec):
    """

    :param l: int
    :param ec: int (<= l, number of errors that will be correctable)
    :return:
    """
    n = l
    while n - needed_redundancy(0, ec, n) != l:
        n += 1
    return n, l, n-l


def parity_check_matrix(k, n, extended=False):
    """
    Generate the parity check matrix (pcm) H that satisfies the requirements for k and n

    :param k: int (number of redundant digits)
    :param n: int (number of overall digits)
    :param extended: bool
    :return: numpy.array (pcm with dimensions k x n)
    """

    # initialize H[n][k] to zero
    if extended:
        n += 1
    h = np.zeros((n, k))
    print(h)
    # fill matrix
    for i in range(1, n + 1):
        binary = list(str(bin(i))[2:].zfill(k))
        h[n - i] = binary

    # transform H into correct human-readable form
    h = h.transpose()
    if extended:
        h = np.append(h, [[1 for i in range(0, n)]], axis=0)

    # rearrange linear independent vectors to create unit matrix
    h_regular = np.fliplr(h)
    for i in range(1, math.floor(math.log(n, 2)) + 1):
        origin = int(math.pow(2, i) - 1)
        h_regular[:, [origin, i]] = h_regular[:, [i, origin]]
    h_regular = np.fliplr(h_regular)

    return h_regular


def generator_matrix(h):
    """
    Generate the generator matrix (gm) G from pcm H

    :param h: numpy.array (parity check matrix with dimension k x n)
    :return: numpy.array (gm with dimensions l x n)
    """

    # get dimensions of H
    k, n = h.shape

    # calculate length of alphabet words from H
    l = n - k

    #
    p = np.delete(h, np.s_[math.ceil(math.log(n, 2))+1:n+1], 1)

    #
    g = np.concatenate((np.identity(l), p.transpose()), axis=1)
    return g


class LHC:
    def __init__(self, l, secded=False):
        """
        Generate HC with error correction 1 and detection 2 (if extended is set 3)
        :param l:
        :param secded:
        :return:
        """
        self.n, self.l, self.k = calc_code(l, 1)
        print(self.n, self.l, self.k)
        self.H = parity_check_matrix(self.k, self.n, extended=True)
        self.G = generator_matrix(self.H)
        print(self)

    def __str__(self):
        return str(self.get_signature()) + ' linear Hamming code generated'

    def get_signature(self):
        """
        Return 3-tuple containing important code parameters
        :return: n, l, k
        """
        return self.n, self.l, self.k

    def encode(self, word):
        """

        :param word: str (will be encoded)
        :return: np.array
        """
        return np.dot(list(map(int, word)), self.G) % 2

    def decode(self, word):
        """

        :param word: str (will be decoded)
        :return: np.array
        """
        return np.dot(self.H, list(map(int, word)).transpose()) % 2
