#!/usr/bin/env python3

import math
from functools import reduce
from collections import Counter
import numpy as np
from markov_source import markov_chain


def runlength(string):

    def runlength_generator(string):
        s_prev = string[0]
        counter = 0
        for s in string:
            if s == s_prev:
                counter += 1
            else:
                yield s_prev, counter
                counter = 1 
                s_prev = s

    ret_array = np.array([])
    for char, length in runlength_generator(string):
        ret_array = np.append(ret_array, [char, length])
    return ret_array

def optimal_bin_code(string):
    optimal_len = lambda p: math.ceil(math.log2(p))
    counter = Counter(string)
    code_len = {key: optimal_len(len(string)/tot) for key, tot in counter.items()}
    return reduce(lambda s, x: s + x[1] * code_len[x[0]], counter.items(), 0)
    

markov = markov_chain(0.2, 0.2, 19600)
code = runlength(markov)
print(code)
print(code.size)
code_len = optimal_bin_code(code)
print(code_len)
