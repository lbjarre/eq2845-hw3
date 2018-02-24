#!/usr/bin/env python3

import sys

import numpy as np
import matplotlib.pyplot as plt

from markov_source import markov_chain
from runlength import runlength, estimate_pmf
from optimals import optimal_encoder, shannon_encoder
from golomb import golomb_encoder
from arithmetic import arithmetic_encoder


ENCODER_STR_FUNC_MAP = {
    'optimal': optimal_encoder,
    'shannon': shannon_encoder,
    'golomb': golomb_encoder,
    'arithmetic': arithmetic_encoder
}

DATA_FILE_MAP = {
    'optimal': 'data/optimal.csv',
    'shannon': 'data/shannon.csv',
    'golomb': 'data/golomb.csv',
    'arithmetic': 'data/arithmetic.csv'
}

PMF_DATA_FILE = 'data/pmf.csv'

SEED_LEN = 15
SOURCE_LEN = 19600

alphas = np.arange(0.05, 0.951, 0.05)

def calc_avg_pmf():
    
    pmfs = np.zeros((1, alphas.size, SEED_LEN))
    
    for seed in range(SEED_LEN):
        np.random.seed(seed)
        for i, a in enumerate(alphas):
            source = markov_chain(a, a, SOURCE_LEN)
            source_runlength = runlength(source)
            pmf = estimate_pmf(source_runlength)
            
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

    pmf_mean = np.mean(pmfs, axis=2)
    pmf_std = np.std(pmfs, axis=2)
    pmf_data = np.column_stack((np.arange(pmfs.shape[0]), pmf_mean, pmf_std))
    
    trunc_prob_str = map(lambda x: '{:.2f}'.format(x)[2:], alphas)
    varnames = ['i'] + ['mean' + s for s in trunc_prob_str] + ['std' + s for s in trunc_prob_str]

    with open(PMF_DATA_FILE, 'w') as f:
        f.write(','.join(varnames) + '\n')
        for data in pmf_data:
            f.write(','.join(map(str, data)) + '\n')

def calc_compr_ratio(encoder, filename):
    
    compr_ratios = np.zeros((alphas.size, SEED_LEN))

    for seed in range(SEED_LEN):
        np.random.seed(seed)
        for i, a in enumerate(alphas):
            source = markov_chain(a, a, SOURCE_LEN)
            _, code_len = encoder(source)
            compr_ratios[i, seed] = SOURCE_LEN / code_len

    compr_mean = np.mean(compr_ratios, axis=1)
    compr_std = np.std(compr_ratios, axis=1)
    compr_data = np.column_stack((alphas, compr_mean, compr_std, compr_ratios))

    varnames = ['alpha', 'mean', 'std'] + ['seed' + str(a) for a in range(SEED_LEN)]

    with open(filename, 'w') as f:
        f.write(','.join(varnames) + '\n')
        for data in compr_data:
            f.write(','.join(map(str, data)) + '\n')


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.stdout.write('Usage: main.py <encoder name>\n')
        sys.exit(1)

    if sys.argv[1] == 'pmf':
        calc_avg_pmf()
    else:
        calc_compr_ratio(ENCODER_STR_FUNC_MAP[sys.argv[1]], DATA_FILE_MAP[sys.argv[1]])

