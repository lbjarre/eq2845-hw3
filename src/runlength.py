#!/usr/bin/env python3

import math
from itertools import groupby
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


def runlength_code(string):
    startval = string[0]
    ret_array = np.array([startval])
    for _, g in groupby(string):
        ret_array = np.append(ret_array, sum(1 for _ in g))
    return ret_array

markov = markov_chain(0.2, 0.2, 19600)
code = runlength_code(markov)
print(code)
print(code.size)
