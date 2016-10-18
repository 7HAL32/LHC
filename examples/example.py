import math
import numpy as np
from hc_gen import LHC

"""
Example showing the generation of a linear Hamming code with a desired
word length of 5 and the capability to correct one mistake
"""
length = 5
code = LHC(length, 1)
print('generator matrix is')
print(code.G)
print('control matrix is')
print(code.H)
with open('input.txt', 'w') as f:
    for number in range(0, int(math.pow(2, length))):
        print(number)
        binary = str(bin(number))[2:].zfill(length)
        temp = ""
        for x in np.nditer(code.encode(binary)):
            temp += str(int(x))
        f.write(temp + '\n')
f.close()
