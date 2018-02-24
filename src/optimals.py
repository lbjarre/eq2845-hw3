#!/usr/bin/env python3

import math
from functools import reduce
from collections import Counter

from runlength import runlength, estimate_pmf

def optimal_encoder(string):
    
    string = runlength(string)
    pmf = estimate_pmf(string)
    symb_len_optimal = {symb: math.log2(1 / prob) for symb, prob in pmf.items()}
    code_len = reduce(
        lambda acc, kv: acc + symb_len_optimal[kv[0]] * kv[1],
        Counter(string).items(),
        0
    )
    return None, code_len

def shannon_encoder(string):
    
    string = runlength(string)
    pmf = estimate_pmf(string)
    symb_len_shannon = {symb: math.ceil(math.log2(1 / prob)) for symb, prob in pmf.items()}
    code_len = reduce(
        lambda acc, kv: acc + symb_len_shannon[kv[0]] * kv[1],
        Counter(string).items(),
        0
    )
    return None, code_len

