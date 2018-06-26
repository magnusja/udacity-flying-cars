import numpy.linalg as LA
from sklearn.neighbors import KDTree

from sampler import Sampler
import networkx as nx
from shapely.geometry import LineString


def can_connect(p1, p2, polygons):
    line = LineString([p1, p2])
    for p in polygons:
        if p.crosses(line) and p.height >= min(p1[2], p2[2]):
            return False
    return True


def create_graph(nodes, polygons, k=5):
    g = nx.Graph()
    tree = KDTree(nodes)
    for n in nodes:
        indicies = tree.query([n], k, return_distance=False)[0]
        
        for i in indicies:
            target_node = nodes[i]
            if n == target_node:
                continue
            
            if can_connect(n, target_node, polygons):
                g.add_edge(tuple(n), tuple(target_node), weight=1)

    return g


def prm(data, num_samples=1000, extra_points=[]):
    sampler = Sampler(data)
    nodes = sampler.sample(num_samples=num_samples)
    print('# sampled nodes {}'.format(len(nodes)))

    nodes += extra_points

    return create_graph(nodes, sampler.polygons), nodes