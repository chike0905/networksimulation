import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

G = nx.Graph()

G.add_edges_from([["0","1"],["1","2"]])

for i in range(3,101):
  G.add_node(str(i))

embed()
