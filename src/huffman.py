#!/usr/bin/env python3

from collections import Counter
import numpy as np

class Node:
    def __init__(self, prob, children=[]):
        self.parent = None
        self.children = children
        self.prob = prob
        for child in children:
            child.parent = self

def huffman(probs):
    active_nodes = [Node(prob) for prob in probs]
    while len(active_nodes) > 1:
        low1 = min(active_nodes, key=lambda x: x.prob)
        active_nodes.remove(low1)
        low2 = min(active_nodes, key=lambda x: x.prob)
        active_nodes.remove(low2)
        new_node = Node(low1.prob + low2.prob, [low1, low2])
        active_nodes.append(new_node)
    return active_nodes[0]

def get_codewords(node, code, codewords):
    if not node.children:
        codewords.append(code)
    else:
        get_codewords(node.children[0], code + '0', codewords)
        get_codewords(node.children[1], code + '1', codewords)
    return codewords


probs = 1/100 * np.ones(100)
root = huffman(probs)
codewords = get_codewords(root, '', [])
codeword_len = [len(c) for c in codewords]
print(Counter(codeword_len))

