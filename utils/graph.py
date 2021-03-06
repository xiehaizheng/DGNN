import torch
import torch.nn.functional as F

class Graph():

    def __init__(self, dataset = 'openpose', strategy = 'spatial'):
        self.dataset = dataset
        self.strategy = strategy
        self.get_edges()
        self.get_adj()

    def get_edges(self):
        if self.dataset == 'openpose':
            self.nodes = [i for i in range(18)]
            self.neighbor_links = [(1, 2), (2, 3), (3, 4), (2, 8), (8, 9), (9, 10), (1, 0),
                    (0, 14), (14, 16), (0, 15), (15, 17), (1, 5), (5, 11),
                    (11, 12), (12, 13), (5, 6), (6, 7)]
            self.self_loops = [(i, i) for i in self.nodes]
            self.edges = self.neighbor_links + self.self_loops

        elif self.dataset == 'ntu-rgbd':
            self.nodes =[i for i in range(25)]
            edges = [(2, 1), (21, 2), (21, 3), (3, 4), (21, 5), (5, 6), (6, 7),
                    (7, 8), (21, 9), (9, 10), (10, 11), (11, 12), (1, 13),
                    (13, 14), (14, 15), (15, 16), (1, 17), (17, 18), (18, 19),
                    (19, 20), (23, 22), (8, 23), (25, 24), (12, 25)]
            self.self_loops = [(i, i) for i in self.nodes]
            self.neighbor_links = [(i - 1, j - 1) for (i, j) in edges]
            self.edges = self.neighbor_links + self.self_loops

        self.num_v = len(self.nodes)
        self.num_e = len(self.edges)

    def get_adj(self):
        adj_source = adj_target = torch.zeros(len(self.nodes), len(self.edges))
        for i in len(self.edges):
            source, target = edges[i]
            adj_source[source][i] = 1.
            adj_target[target][i] = 1.
        if strategy = 'uniform':
            self.adj_source = F.normalize(adj_source, p = 1)
            self.adj_target = F.normalize(adj_target, p = 1)
        elif strategy = 'spatial':
            adj_source[:, :len(self.neighbor_links)] = self.normalize_adj(adj_source[:, :len(self.neighbor_links)])
            adj_target[:, :len(self.neighbor_links)] = self.normalize_adj(adj_target[:, :len(self.neighbor_links)])
            self.adj_source, self.adj_target = adj_source, adj_target

    def normalize_adj(self, A):
        m = torch.sum(A, 1)
        for i in range(self.nodes):
            A[i] =/ m[i]
        return A
