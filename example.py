from LHC import LHC

"""
Example showing the generation of a linear Hamming code with a desired
word length of 5 and the capability to correct one mistake
"""

code = LHC(5,1)
print('generator matrix is')
print(code.G)
print('control matrix is')
print(code.H)
print(code.encode('10101'))
