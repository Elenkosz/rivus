# See: https://docs.python.org/3/tutorial/modules.html#packages
# Create more inteligent way of importting module components
from .to_graph import to_nx, to_igraph

__all__ = ["to_nx", "to_igraph"]
