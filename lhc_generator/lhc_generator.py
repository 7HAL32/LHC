"""
Package: 7HAL32/lhc_generator

Generates linear Hamming codes by the required source alphabet word length. Optionally an extended SECDED code may be created by passing the extended flag during initialisation.

This tool is used to create the extended linear Hamming code that secures the reading/transmission of machine words of the stack machine robot which is designed, assembled and programmed by students during the NES RoboLab course at Technische Universität Dresden. Specifications and further information can be found at http://robolab.inf.tu-dresden.de (reachable from within campus network).

Developed as part of the NES RoboLab Project at Technische Universität Dresden.
Handcrafted with :heart: by Lutz Thies in 2016.
"""

import math
import numpy

from .code_tools import construct_code
from .is_power_of_two import is_power_of_two
from .hcresult import HCResult
from .parity import parity

__author__ = "Lutz Thies"
__copyright__ = "Copyright (c) 2016"
__credits__ = ["Lutz Thies"]

__license__ = "MIT"
__version__ = "1.2.2"
__maintainer__ = "Lutz Thies"
__email__ = "lutz.thies@tu-dresden.de"
__status__ = "Release"


class LHC:
    def __init__(self, l, extended=True):
        """
        Generates a Hamming code with single error correction and detection for the specified word length.
        If extended was set, an additional parity bit will be appended, thus increasing the error detection capability by one making the generated code a SECDED Hamming code.

        :param l: int (source alphabet word length)
        :param extended: bool (flag for SECDED)
        :returns: %
        """

        # calculate necessary code parameters
        self.n, self.l, self.k = construct_code(l, 1)

        # calculate the matrices
        self.H = self.parity_check_matrix(self.n, self.k)
        self.G = self.generator_matrix(self.H)

        # increase visible code parameters after generation
        self.extended = extended
        if self.extended:
            self.n += 1
            self.k += 1

        # tell us who you are
        print(self)

    def __str__(self):
        return str(self.get_signature()) + ' linear Hamming code generated.'

    def get_signature(self):
        """
        Returns 3-tuple containing the code signature (i.e. most defining code parameters)
        :return: n, l, k
        """
        return self.n, self.l, self.k

    @staticmethod
    def parity_check_matrix(n, k):
        """
        Generates the parity check matrix (PCM) H satisfying the requirements for k and n

        :param k: int (number of redundant digits)
        :param n: int (number of overall digits)
        :returns: numpy.array (PCM with dimensions k x n)
        """

        # initialize H_reduced to zero
        h_reduced = numpy.zeros((n - k, k), dtype=int)

        # fill H
        counter = 0
        for i in range(n, 2, -1):
            if not is_power_of_two(i):
                h_reduced[counter] = list(str(bin(i))[2:].zfill(k))
                counter += 1

        # append unit matrix to complete the PCM
        h = numpy.concatenate((h_reduced, numpy.identity(k)), axis=0)

        # return H in human-readable form
        return h.transpose().astype(int)

    @staticmethod
    def generator_matrix(h):
        """
        Generates the generator matrix (GM) G from PCM H

        :param h: numpy.array (PCM with dimensions k x n)
        :returns: numpy.array (GM with dimensions l x n)
        """
        # get dimensions of H
        k, n = h.shape
        # calculate length of alphabet words from H
        l = n - k
        # remove all powers of two
        p = numpy.delete(h, numpy.s_[math.ceil(math.log(n, 2)) + 1:n + 1], 1)
        # append unit matrix of dimensions l x l
        g = numpy.concatenate((numpy.identity(l), p.transpose()), axis=1)
        return g.astype(int)

    def typing(self, word, encoded):
        """
        Casts the input to type list that is used internally

        :param word: int or list or str or tuple
        :param encoded: bool (determines which lenght is used for padding)
        :returns: list
        """
        # original type
        t = type(word)

        if t == int:
            print("WARNING, you are using integers for direct input")
            print("Padding with zeros to the necessary length may occur, errors in input length cannot be recognized!")
            length = self.n if encoded else self.l
            word = map(int, str(word).zfill(length))
        elif t is str:
            word = map(int, word)

        # not explicitly mentioned cases: list, tuple
        return list(word)

    def encode(self, word):
        """
        Encodes a source alphabet word

        :param word: int or list or str or tuple (will be encoded)
        :returns: tuple (the encoded channel code word)
        """
        # prepare for different types
        word = self.typing(word, encoded=False)

        # calculate encoded word: e = word * G
        e = numpy.dot(word, self.G) % 2

        # append additional overall parity bit
        if self.extended:
            e = numpy.append(e, [parity(e)])

        return tuple(e.astype(int))

    def decode(self, word):
        """
        Attempts to decode channel code words, returns a status code indicating the level of error in addition to the decoded word.

        In case of extended LHC:
        # Errors      Overall parity  Syndrome        Type
        0              0 (even)           0           no error
        1              1 (odd)            0           overall parity bit is in error
        1              1 (odd)           =!0          single error (correctable via syndrome)
        >1             1 (odd)    !=0 && not in H     multiple errors
        >1             0 (even)          !=0          multiple errors

        :param word: tuple or int or str (channel code word with length l)
        :returns: tuple(tuple, HCResult) or tuple (None, HCResult)
        """
        # prepare for different types
        word = self.typing(word, encoded=True)

        # extended LHC with additional overall parity check
        additional_parity = True
        if self.extended:
            # even parity
            additional_parity = parity(word)
            # remove additional parity bit
            word = word[:-1]

        # check if syndrome is zero by calculating matrix vector product H * w^T
        s = numpy.dot(self.H, numpy.array([word]).transpose()) % 2
        s_is_zero = numpy.count_nonzero(s) == 0

        if s_is_zero:
            # fake "correction" of parity bit or valid
            return tuple(word[:5]), HCResult.corrected if additional_parity else HCResult.valid
        else:
            # look up syndrome in H
            position = numpy.where(numpy.all(s == self.H, axis=0))[0]
            if position.shape == (0,) or not additional_parity:
                # multiple errors -> uncorrectable
                return None, HCResult.uncorrectable

            # single error -> correctable
            idx = numpy.squeeze(position[0])
            word[idx] = int(not word[idx])
            return tuple(word[:5]), HCResult.corrected
