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

def optimal_encoder(string):
    counter = Counter(string)
    str_len = len(string)
    pdf = dict(map(
        lambda kv: (kv[0], kv[1]/str_len),
        counter.items()
    ))
    optimal_lens = dict(map(
        lambda kv: (kv[0], math.ceil(math.log2(1/kv[1]))),
        pdf.items()
    ))
    tot_len = reduce(
        lambda acc, kv: acc + kv[1] * optimal_lens[kv[0]],
        counter.items(),
        0
    )

    return tot_len, pdf
    
