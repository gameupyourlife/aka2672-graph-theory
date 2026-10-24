"""Shared library for the graph theory course ("Aka Kunterbunt").

The most important names can be imported directly from ``lib``::

    from lib import Graph, Edge

Modules:

* :mod:`lib.graph` - the :class:`Graph` class (adjacency lists)
* :mod:`lib.generators` - example graphs (paths, cycles, random graphs, ...)
* :mod:`lib.visualization` - text output and Graphviz DOT export
* :mod:`lib.testing` - checks for paths, trees, colourings, matchings, flows
* :mod:`lib.utils` - small helpers (loading other exercises, timing, ...)
"""

from lib.graph import Edge, Graph, Vertex

__all__ = ["Edge", "Graph", "Vertex"]
