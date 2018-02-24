#!/usr/bin/env

import math
from functools import reduce

import numpy as np

from runlength import pmf_estimate


def plogp(p):
    if p == 0:
        return 0
    return p * math.log2(p)

def estimate_entropy(string):
    pmf = pmf_estimate(string)
    return reduce(
        lambda acc, prob: acc - plogp(prob),
        pmf.values(),
        0
    )

def estimate_rate(string, size): 
    estimate = np.zeros(string.shape)
    block = deque(string[0: size])
    p1 = np.count_nonzero(block)/size
    p0 = 1 - p1
    estimate[size-1] = - plogp(p0) - plogp(p1)
    for i in range(size, len(string)):
        block.append(string[i])
        block.popleft()
        p1 = np.count_nonzero(block)/size
        p0 = 1 - p1
        estimate[i] = - plogp(p0) - plogp(p1)
    return estimate
