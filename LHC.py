import math
import numpy as np
from nCk import nCk

def calc_redundancy(i, k, n):
    sum=0
    for x in range(i, k + 1):
        sum += nCk(n, x)
    return math.ceil(math.log(sum, 2))

def H_from_code(k,n):
    # initialize matrix and fill it
    H = np.zeros((n,k))
    for i in range(1,n + 1):
        binary = list(str(bin(i))[2:].zfill(k))
        H[n - i] = binary
    H = H.transpose()
    H_reg = np.fliplr(H)
    # rearrange linear independent vectors to create unit matrix
    for i in range(1,math.floor(math.log(n,2)) + 1):
        origin = int(math.pow(2,i) - 1)
        H_reg[:,[origin,i]] = H_reg[:,[i,origin]]
    H_reg = np.fliplr(H_reg)
    return H_reg

def G_from_H(H,l):
    k, n = H.shape
    P = np.delete(H,np.s_[math.ceil(math.log(n,2))+1:n+1],1)
    return np.concatenate((np.identity(l),P.transpose()),axis=1)

def calc_code(l, fk):
    n = l
    while n - calc_redundancy(0,fk,n) != l:
        n += 1
    return n, l, n-l

class LHC:
    def __init__(self, l, fk):
        self.n, self.l, self.k = calc_code(l,fk)
        self.H = H_from_code(self.k, self.n)
        self.G = G_from_H(self.H, self.l)
        print(self)
    def __str__(self):
        return str(self.getParams()) + ' linear Hamming code generated'

    def getParams(self):
        """ return the common (n, l, k) representation of this code """
        return self.n, self.l, self.k

    def encode(self, w):
        return np.dot(list(map(int, w)), self.G) % 2

    def decode(self, w):
        return np.dot(self.H,list(map(int, w)).transpose()) % 2
