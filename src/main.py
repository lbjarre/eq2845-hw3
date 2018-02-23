#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from markov_source import markov_chain
from runlength import runlength, optimal_encoder


COMPR_DATA_FILE = 'data/optimal.csv'
PMF_DATA_FILE = 'data/pmf.csv'

SEED_LEN = 15
SOURCE_LEN = 19600

alphas = np.arange(0.05, 0.951, 0.05)

clen = np.zeros((alphas.size, SEED_LEN))
pmfs = np.zeros((1, alphas.size, SEED_LEN))

for seed in range(SEED_LEN):
    np.random.seed(seed)
    print(seed)
    for i, a in enumerate(alphas):
        source = markov_chain(a, a, SOURCE_LEN)
        source_runlength = runlength(source)
        code_len, pmf = optimal_encoder(source_runlength)
        clen[i, seed] = SOURCE_LEN / code_len

        pmf_vec_len = max(pmf.keys()) + 1
        pmf_vec = np.zeros(int(pmf_vec_len))
        for k, p in pmf.items():
            pmf_vec[int(k)] = p
        pmf_shape_diff = pmfs.shape[0] - pmf_vec.shape[0]
        if pmf_shape_diff < 0:
            pmfs = np.pad(pmfs, ((0, -pmf_shape_diff), (0, 0), (0, 0)), 'constant')
        elif pmf_shape_diff > 0:
            pmf_vec = np.pad(pmf_vec, (0, pmf_shape_diff), 'constant')
        for k, p in enumerate(pmf_vec):
            pmfs[k, i, seed] = p

compr_mean = np.mean(clen, axis=1)
compr_std = np.std(clen, axis=1)
compr_data = np.column_stack((alphas, compr_mean, compr_std, clen))

pmf_mean = np.mean(pmfs, axis=2)
pmf_std = np.std(pmfs, axis=2)
pmf_data = np.column_stack((np.arange(pmfs.shape[0]), pmf_mean, pmf_std))

with open(COMPR_DATA_FILE, 'w') as f:
    varnames = ['alpha', 'mean', 'std'] + ['seed' + str(a) for a in range(SEED_LEN)]
    f.write(','.join(varnames) + '\n')
    for data in compr_data:
        f.write(','.join([str(d) for d in data]) + '\n')

with open(PMF_DATA_FILE, 'w') as f:
    varnames = ['i'] + ['mean' + '{:.2f}'.format(a)[2:] for a in alphas] + ['std' + '{:.2f}'.format(a)[2:] for a in alphas]
    f.write(','.join(varnames) + '\n')
    for data in pmf_data:
        f.write(','.join([str(d) for d in data]) + '\n')
