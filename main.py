import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import pylab
import random

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

def showgraph(G):
  pos = nx.spring_layout(G)
  nx.draw_networkx_nodes(G, pos, node_size=100, node_color="r")
  nx.draw_networkx_edges(G, pos, width=1)
  plt.show()
  return 0


def random_weight_choice(L):
    choice = None
    total = 0
    for item, p in L:
        total += p
        if random.random() * total < p:
            choice = item
    return choice

def BasicSelection(G):
  C = []
  degree = nx.degree(G)
  degreeitem = degree.items()
  for a in degreeitem:
    alldegree = float()
    for i in degreeitem:
      alldegree = alldegree + float(i[1])
    C.append((a[0],float(a[1])/alldegree))
  return random_weight_choice(C)

def LengthSelection(G,node):
  Lengthdict = nx.single_source_dijkstra_path_length(G,node)
  sl = sort(Lengthdict)
  candidate = []
  for a in sl:
    if sl[0][1] is a[1]:
      candidate.append(a[0])
  return candidate[random.randint(1,len(candidate)) - 1]

def RandAddNode(G,i):
  G.add_edge(str(i),str(random.randint(0,i)))
  G.add_edge(str(i),str(random.randint(0,i)))

def WeigthAddNode(G,i):
  G.add_edge(str(i),str(random.randint(0,i)))
  G.add_edge(str(i),str(BasicSelection(G)))

def LengthAddNode(G,i):
  G.add_edge(str(i),str(random.randint(0,i)))
  G.add_edge(str(i),str(LengthSelection(G,str(i))))

def sort(map):
  ms=sorted(map.iteritems(), key=lambda (k,v): (-v,k))
  return ms


randG = [nx.Graph() for a in range(10)]
weigthG = [nx.Graph() for a in range(10)]
lengthG = [nx.Graph() for a in range(10)]

randCC = [None for a in range(10)]
weigthCC = [None for a in range(10)]
lengthCC = [None for a in range(10)]

for a in range(10):
  randG[a].add_nodes_from(range(1000))
  weigthG[a].add_nodes_from(range(1000))
  lengthG[a].add_nodes_from(range(1000))
  randG[a].add_edges_from([(0,1),(1,2)])
  weigthG[a].add_edges_from([(0,1),(1,2)])
  lengthG[a].add_edges_from([(0,1),(1,2)])

  randCC[a] = [[] for row in range(1000)]
  weigthCC[a] = [[] for row in range(1000)]
  lengthCC[a] = [[] for row in range(1000)]

  for i in range(3):
    randCC[a][i].append(nx.average_clustering(randG[a]))
    weigthCC[a][i].append(nx.average_clustering(weigthG[a]))
    lengthCC[a][i].append(nx.average_clustering(lengthG[a]))

for a in range(10):
  for i in range(3,1000):
    RandAddNode(randG[a],i)
    WeigthAddNode(weigthG[a],i)
    LengthAddNode(lengthG[a],i)
    randCC[a][i].append(nx.average_clustering(randG[a]))
    weigthCC[a][i].append(nx.average_clustering(weigthG[a]))
    lengthCC[a][i].append(nx.average_clustering(lengthG[a]))

rave = []
wave = []
lave = []

for a in range(1000):
  add = [0,0,0]
  for i in range(10):
    add[0] = add[0] + float(randCC[i][a][0])
    add[1] = add[1] + float(weigthCC[i][a][0])
    add[2] = add[2] + float(lengthCC[i][a][0])
  rave.append(add[0]/10)
  wave.append(add[1]/10)
  lave.append(add[2]/10)

embed()
