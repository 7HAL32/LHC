import math
import numpy as np
from .code_tools import construct_code
from .is_power_of_two import is_power_of_two


def parity_check_matrix(n, k):
    """
    Generate the parity check matrix (PCM) H that satisfies the requirements for k and n

    :param k: int (number of redundant digits)
    :param n: int (number of overall digits)
    :return: numpy.array (pcm with dimensions k x n)
    """

    # initialize H_reduced to zero
    h_reduced = np.zeros((n - k, k), dtype=int)

    # fill H
    counter = 0
    for i in range(n, 2, -1):
        if not is_power_of_two(i):
            h_reduced[counter] = list(str(bin(i))[2:].zfill(k))
            counter += 1

    # append unit matrix to complete the PCM
    h = np.concatenate((h_reduced, np.identity(k)), axis=0)

    # transform H into correct human-readable form
    h = h.transpose()
    return h


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


def parity(bitsequence):
    p = 0
    b = list(map(int, bitsequence))

    for bit in b:
        p ^= int(bit)

    return p


class LHC:
    def __init__(self, l, extended=True):
        """
        Generate HC with error correction 1 and detection 2 (if extended is set 3)
        :param l:
        :param extended: bool
        :return:
        """
        self.extended = extended
        self.n, self.l, self.k = construct_code(l, 1)
        print(self.n, self.l, self.k)
        self.H = parity_check_matrix(self.n, self.k)
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
        word = str(word)
        final = np.dot(list(map(int, word)), self.G) % 2
        if self.extended:
            final = np.append(final, [parity(final)])
        return final

    def decode(self, word):
        """
        Decodes received code words and provides error information
        In case of EHC:
        # Errors Overall parity Syndrome
        0             odd           0       No error
        1             even          0       Overall parity bit is in error
        1             even          1       Single error (correctable via syndrome)
        2             odd           0       Double error (not correctable)
        3             even       not in H   Triple error

        :param word: str (will be decoded)
        :return: np.array
        """
        word = str(word)
        if self.extended:
            if parity(word) == 1:
                print("even")
            else:
                print("odd")
            word = word[0:-1]


        sequence = list(map(int, word))
        return np.dot(self.H, np.array([sequence]).transpose()) % 2
