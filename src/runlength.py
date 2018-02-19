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

    def runlength_generator(string):
        s_prev = None
        counter = 1
        for s in string:
            if s == s_prev:
                counter += 1
            else:
                yield counter
                counter = 1 
                s_prev = s

    ret_array = np.array(string[0])
    ret_array = np.append(ret_array, [l for l in runlength_generator(string)])
    return ret_array

markov = markov_chain(0.2, 0.2, 19600)
code = runlength_code(markov)
print(code)
print(code.size)
