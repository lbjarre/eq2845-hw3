#!/usr/bin/env python3

import math
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

def estimate_pmf(string):
    counter = Counter(string)
    str_len = len(string)
    return dict(map(
        lambda kv: (kv[0], kv[1] / str_len),
        counter.items()
    ))

