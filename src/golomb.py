#!/usr/bin/env python3

import math

from runlength import runlength

def golomb_encoder(string):

    encoded = ''

    n = 1
    avg_estimate = 10
    n_max = 100

    for i, s in enumerate(runlength(string)):
        s = int(s)
        k = max(0, math.ceil(math.log2(avg_estimate/(2*n))))
        unary = math.floor(s/2**k)
        const = s % 2**k
        encoded += '0' * unary + '1' + '{:b}'.format(const)

        if n == n_max:
            avg_estimate = math.floor(avg_estimate/2)
            n = math.floor(n/2)

        avg_estimate += s
        n += 1
    
    return encoded, len(encoded)

