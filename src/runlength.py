#!/usr/bin/env python3

import math
from functools import reduce
from collections import Counter
import numpy as np

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
    counter = Counter(string)
    optimal_len = lambda p: math.ceil(math.log2(p))
    code_len = {key: optimal_len(len(string)/tot) for key, tot in counter.items()}
    return reduce(lambda s, x: s + x[1] * code_len[x[0]], counter.items(), 0)
    
