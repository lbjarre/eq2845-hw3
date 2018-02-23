#!/usr/bin/env python3

import math
import numpy as np

from markov_source import markov_chain
from runlength import runlength

def golomb(string):

    encoded = ''

    n = 1
    avg_estimate = 10
    n_max = 100

    for i, s in enumerate(string):
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
    
    return encoded

source_len = 19400

source = markov_chain(0.05, 0.05, source_len)
source_runlength = runlength(source)
encoded = golomb(source_runlength)
print(source_len / len(encoded))
