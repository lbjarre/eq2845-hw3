#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from markov_source import markov_chain
from runlength import runlength, optimal_bin_code

SOURCE_LEN = 19600

alphas = np.arange(0.05, 0.95, 0.05)

clen = np.zeros(alphas.shape)

for i, a in enumerate(alphas):
    source = markov_chain(a, a, SOURCE_LEN)
    source_runlength = runlength(source)
    code_len = optimal_bin_code(source_runlength)
    clen[i] = code_len / SOURCE_LEN

plt.plot(alphas, clen)
plt.show()

