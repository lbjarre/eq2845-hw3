#!/usr/bin/env python3

import numpy as np

def markov_chain(a, b, size):
    rnd = np.random.rand(size)
    string = np.zeros(size)
    string[0] = 0 if rnd[0] <= b/(a+b) else 1
    for i in range(1, size):
        if string[i-1] == 0:
            string[i] = 1 if rnd[i] <= a else 0
        else:
            string[i] = 0 if rnd[i] <= b else 1
    return string
