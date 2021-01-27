#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from utils import iterator, reader, normalizer

class RWR():
    def __init__(self):
        pass

    normalized = False
    def read_graph(self, input_path, graph_type):
        '''
        Read a graph from the edge list at input_path
        inputs
            input_path : str
                path for the graph data
            graph_type : str
                type of graph {'directed', 'undirected', 'bipartite'}
        '''  
        self.A, self.base = reader.read_graph(input_path, graph_type)
        self.m, self.n = self.A.shape
        self.node_ids = np.arange(0, self.n) + self.base
        self.normalize()

    def normalize(self):
        '''
        Perform row-normalization of the adjacency matrix
        '''
        if self.normalized is False:
            nA = normalizer.row_normalize(self.A)
            self.nAT = nA.T
            self.normalized = True

    def compute(self, seed, c=0.15, epsilon=1e-6, max_iters=100,
                handles_deadend=True):
        '''
        Compute the RWR score vector w.r.t. the seed node
        inputs
            seed : int
                seed (query) node id
            c : float
                restart probability
            epsilon : float
                error tolerance for power iteration
            max_iters : int
                maximum number of iterations for power iteration
            handles_deadend : bool
                if true, it will handle the deadend issue in power iteration
                otherwise, it won't, i.e., no guarantee for sum of RWR scores
                to be 1 in directed graphs
        outputs
            r : ndarray
                RWR score vector
        '''

        self.normalize()

        # adjust range of seed node id
        seed = seed - self.base

        #  q = np.zeros((self.n, 1))
        q = np.zeros(self.n)
        if seed < 0 or seed >= self.n:
            raise ValueError('Out of range of seed node id')

        q[seed] = 1.0

        r, residuals = iterator.iterate(self.nAT, q, c, epsilon,
                                        max_iters, handles_deadend)

        return r