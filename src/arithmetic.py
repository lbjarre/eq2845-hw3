#!/usr/bin/env python3

import math

def arithmetic_encoder_markov(string, a):
    
    encoded = ''

    N = 22
    P = 8
    
    p_switch= math.floor(a * 2**P)
    p_stay = math.floor((1-a) * 2**P)
    mod_mask = 2**(N + P) - 1

    C = 0
    A = 2**N
    r = -1
    b = 0

    s_prev = 0

    for s in string:
        if s != s_prev:
            T = A * p_switch
        else:
            T = A * p_stay
            C = C + T

        if C >= 2**(N + P):
            C = C & mod_mask
            encoded += '1'
            if r > 0:
                encoded += '0' * (r - 1)
                r = 0
            else:
                r = -1

        while T < 2**(N + P - 1):
            b += 1
            T = T << 1
            C = C << 1
            if C >= 2**(N + P):
                C = C & mod_mask
                if r < 0:
                    encoded += '1'
                else:
                    r += 1
            else:
                if r >= 0:
                    encoded += '0' + '1' * r
                r = 0

        A = math.floor(T >> P)
        s_prev = s
    
    if r >= 0:
        encoded += '0' + '1' * r

    encoded += '{:b}'.format(C)[-(N + P):]
    
    return encoded, len(encoded)


def arithmetic_encoder(string, p0):
    
    encoded = ''

    N = 22
    P = 8
    
    p0 = math.floor(p0 * 2**P)
    mod_mask = 2**(N + P) - 1

    C = 0
    A = 2**N
    r = -1
    b = 0

    for s in string:
        T = A * p0
        if s == 1:
            C = C + T
            T = (A << P) - T

        if C >= 2**(N + P):
            C = C & mod_mask
            encoded += '1'
            if r > 0:
                encoded += '0' * (r - 1)
                r = 0
            else:
                r = -1

        while T < 2**(N + P - 1):
            b += 1
            T = T << 1
            C = C << 1
            if C >= 2**(N + P):
                C = C & mod_mask
                if r < 0:
                    encoded += '1'
                else:
                    r += 1
            else:
                if r >= 0:
                    encoded += '0' + '1' * r
                r = 0

        A = math.floor(T >> P)
    
    if r >= 0:
        encoded += '0' + '1' * r

    encoded += '{:b}'.format(C)[-(N + P):]
    
    return encoded, len(encoded)


