#!/usr/bin/env python3

import math
import ctypes

from markov_source import markov_chain


def arithmetic(string, p0):
    
    encoded = ''

    N = 22
    P = 8
    
    C = 0
    A = 2**N
    r = -1
    b = 0

    for s in string:
        s = int(s)
        T = A * p0
        if s == 1:
            C = C + T
            T = (A << P) - T

        if C >= 2**(N + P):
            C = C % 2**(N + P)
            encoded += '1'
            if r > 0:
                encoded += '0' * (r - 1)
                r = 0
            else:
                r = -1

        while T < 2**(N + P - 1):
            b += 1
            T = 2 * T
            C = 2 * C
            if C >= 2**(N + P):
                C = C % 2**(N + P)
                if r < 0:
                    encoded += '1'
                else:
                    r += 1
            else:
                if r >= 0:
                    encoded += '0' + '1' * r
                r = 0

        A = math.floor(T / 2**P)
    
    if r >= 0:
        encoded += '0' + '1' * r

    encoded += '{:b}'.format(int(C))[-(N + P):]
    
    return encoded

source = markov_chain(0.9, 0.9, 100)
encoded = arithmetic(source, 0.5)
print(len(source))
print(len(encoded))

