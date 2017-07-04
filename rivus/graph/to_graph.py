import os
import igraph as ig
#import networks as nx

"""Functions to convert tabular data to graph formats"""


def to_igraph(vdf, edf, pmax, comms=None, peak=None, save_dir=None, ext='gml'):
    """Convert Data from (Geo)DataFrames to igraph(s)
    Each commodity gets its own graph
    Weights are derived from built capacity.

    Args:
        vdf ([Geo]DataFrame): Holding Vertex Data id=Vertex
            and Commodity Sources as columns
        edf ([Geo]DataFrame): Holding (V1,V2) Multi-indexed Edge data
        pmax (DataFrame): Commodities as columns with max capacity per edge
            returned by rivus.get_constants()
        comms (iterable, optional): Names of commodities
        peak (DataFrame, optional): Commodities as columns with demands
            in t_peak time-step. Calculated in main.rivus
        save_dir (path string, optional): Path to a dir to save graphs as GML
            Path preferably constructed with use of os.path module
            If dir does not exit yet, it will be created.
        ext (string) file extension, supported by igraph.save()
            If not one of the following, the default 'gml' will be applied.
            'adjacency', 'dimacs', 'dot', 'graphviz', 'edgelist', 'edges', 
            'edge', 'gml', 'graphml', 'graphmlz', 'gw', 'leda', 'lgl', 'lgr', 
            'ncol', 'net', 'pajek', 'pickle', 'picklez', 'svg'

    Returns:
        List of igraph.Graph objects in order of `comms`
    """
    ext_list = ['adjacency', 'dimacs', 'dot', 'graphviz', 'edgelist', 'edges',
                'edge', 'gml', 'graphml', 'graphmlz', 'gw', 'leda', 'lgl',
                'lgr', 'ncol', 'net', 'pajek', 'pickle', 'picklez', 'svg']
    if ext not in ext_list:
        ext = 'gml'
    if len(edf) != len(pmax):
        pmax = edfr.join(pmax).fillna(0)
    comms = pmax.columns.values if comms == None else comms

    graphs = []
    for comm in comms:
        g = ig.Graph()
        g['name'] = '{} capacity graph'.format(comm.upper())
        g['commodity'] = comm
        # Vertices added separately not constructed with Graph(edges)
        # to make sure possible isolated vertices are also included.
        g.add_vertices(len(vdf))
        g.vs['Label'] = vdf.index.values.tolist()
        g.vs[comm] = vdf[comm].tolist()
        g.add_edges(edf.index.values.tolist())
        g.es['Label'] = list(map(lambda v1v2: '{}-{}'.format(*v1v2),
                                 edf.index.values))
        g.es[comm] = pmax[comm].tolist()
        weights = pmax[comm] / pmax[comm].max()
        g.es['weight'] = weights.tolist()
        if peak != None:
            g.es[comm + '-peak'] = peak[comm].tolist()
        # For possible GeoLayout (e.g. in Gephi)
        g.vs['longitude'] = vdf.geometry.map(lambda p: p.x).tolist()
        g.vs['latitude'] = vdf.geometry.map(lambda p: p.y).tolist()
        graphs.append(g)

    if save_dir:
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        for graph in graphs:
            gpath = os.path.join(save_dir, '{}.{}'.format(graph['name']), ext)
            with open(gpath, 'w') as fhandle:
                graph.save(fhandle, ext)
    return graphs


def to_nx(vdf, edf, pmax, save_as=None):
    pass
