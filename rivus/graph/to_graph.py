import igraph as ig
#import networks as nx


def to_igraph(vdf, edf, pmax, flows=None, saveas=None):
    """Convert Data from DataFrames to igraph
    
    Args:
        vdf ([geo]dataframe): Holdin Vertex Data id=Vertex
        	and Comodity Sources as columns
        edf ([geo]dataframe): Holding (V1,V2) Multiindexed Edge data
        Pmax (dataframe): Commodities as Columns with max capacity per edge
        	returned by rivus.get_constants()
    Returns:
    	igraph.Graph object
    """
    g = ig.Graph()  # not directly from edges, to save isolated vertices
    g.add_vertices(len(vdf))
    g.add_edges(edf.index.values.tolist())
    comms = pmax.columns.values  # Which are built out in optimum
	# if pmax is not already len(edge) long
	# pmax = edfr.join(prob['pmax']).fillna(0)
	for comm in comms:
	    g.vs[comm] = vdfr[comm].tolist()
	    g.es[comm] = pmax[comm].tolist()
	    if comm in prob['peak'].columns.values:
	        g.es[comm + '_peak'] = prob['peak'][comm].tolist()

	return g

def to_nx(vdf, edf, pmax, flows=None, saveas=None):
	pass
