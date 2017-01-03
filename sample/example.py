#!/usr/bin/env python3

"""
Package: 7HAL32/lhc_generator

Example demonstrating the generation of a linear Hamming code with a desired word length of 5 and the capability to correct one error. Outputs all code words to ./output.txt.

Developed as part of the NES RoboLab Project at Technische Universität Dresden.
Handcrafted with :heart: by Lutz Thies in 2016.
"""

import math
from lhc_generator import LHC

# generate linear extended Hamming code with source alphabet word length 5
length = 5
code = LHC(l=length, extended=True)
print('generator matrix is')
print(code.G)
print('control matrix is')
print(code.H)
# generate all code words and dump them into output.txt
with open('output.txt', 'w') as f:
    for number in range(0, int(math.pow(2, length))):
        binary = str(bin(number))[2:].zfill(length)
        f.write(''.join(str(x) for x in code.encode(binary)) + '\n')
f.close()
