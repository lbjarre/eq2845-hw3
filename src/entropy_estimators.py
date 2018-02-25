#!/usr/bin/env python3

import math
from functools import reduce
from collections import deque

import numpy as np

from runlength import estimate_pmf
from markov_source import markov_chain
from arithmetic import arithmetic_encoder_markov


DATA_FILE_ENTROPY_SOURCE = 'data/entropy.csv'
DATA_FILE_RATE_SOURCE = 'data/rate.csv'

SEED_LEN = 15
SOURCE_LEN = 20000

RATE_BLOCK_SIZE = 10

alphas = np.arange(0.05, 0.951, 0.05)

def plogp(p):
    if p == 0:
        return 0
    return p * math.log2(p)

def estimate_entropy(string):
    pmf = estimate_pmf(string)
    return reduce(
        lambda acc, prob: acc - plogp(prob),
        pmf.values(),
        0
    )

def estimate_rate(string, size): 
    estimate = np.zeros(len(string))
    block = deque(string[0: size])
    p1 = np.count_nonzero(block)/size
    p0 = 1 - p1
    estimate[size-1] = - plogp(p0) - plogp(p1)
    for i in range(size, len(string)):
        block.append(string[i])
        block.popleft()
        p1 = np.count_nonzero(block)/size
        p0 = 1 - p1
        yield i, - plogp(p0) - plogp(p1)

if __name__ == '__main__':

    entropy_source = np.zeros((alphas.size, SEED_LEN))
    entropy_code = np.zeros((alphas.size, SEED_LEN))
    rate_source = np.zeros((SOURCE_LEN, alphas.size, SEED_LEN))
    rate_code = np.zeros((SOURCE_LEN * 2, alphas.size, SEED_LEN))

    for seed in range(SEED_LEN):
        print(seed)
        np.random.seed(seed)
        for i, a in enumerate(alphas):
            source = markov_chain(a, a, SOURCE_LEN)
            code, _ = arithmetic_encoder_markov(source, a)
            entropy_source[i, seed] = estimate_entropy(source)
            entropy_code[i, seed] = estimate_entropy(code)
            #for n, rate in estimate_rate(source, RATE_BLOCK_SIZE):
            #    rate_source[n, i, seed] = rate
            #for n, rate in estimate_rate(code, RATE_BLOCK_SIZE):
            #    rate_code[n, i, seed] = rate

    entropy_source_mean = np.mean(entropy_source, axis=1)
    entropy_source_std = np.std(entropy_source, axis=1)
    entropy_code_mean = np.mean(entropy_code, axis=1)
    entropy_code_std = np.std(entropy_code, axis=1)
    
    entropy_data = np.column_stack((
        alphas,
        entropy_source_mean, entropy_source_std,
        entropy_code_mean, entropy_code_std
    ))

    varnames = ['alpha', 's_mean', 's_std', 'c_mean', 'c_std']

    with open(DATA_FILE_ENTROPY_SOURCE, 'w') as f:
        f.write(','.join(varnames) + '\n')
        for data in entropy_data:
            f.write(','.join(map(str, data)) + '\n')

