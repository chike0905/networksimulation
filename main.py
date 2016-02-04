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
  G.add_edge(str(i),str(random.randint(0,10)))

def WeigthAddNode(G,i):
  G.add_edge(str(i),str(BasicSelection(G)))

def LengthAddNode(G,i):
  length = nx.single_source_dijkstra_path_length(G,str(i))
  flag = []
  for a in length.keys():
    neigh = G.neighbors(str(i))
    flag.append(a in neigh)
  if True in neigh:
    G.add_edge(str(i),str(LengthSelection(G,str(i))))
  else:
    G.add_edge(str(i),str(random.randint(0,10)))

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
  for i in range(0,12,3):
    randG[a].add_edges_from([(str(i),str(i+1)),(str(i+1),str(i+2))])
    weigthG[a].add_edges_from([(str(i),str(i+1)),(str(i+1),str(i+2))])
    lengthG[a].add_edges_from([(str(i),str(i+1)),(str(i+1),str(i+2))])

  randCC[a] = [0.0 for row in range(100)]
  weigthCC[a] = [0.0 for row in range(100)]
  lengthCC[a] = [0.0 for row in range(100)]


  for i in range(4):
    randCC[a][i] = nx.average_clustering(randG[a])
    weigthCC[a][i] = nx.average_clustering(weigthG[a])
    lengthCC[a][i] = nx.average_clustering(lengthG[a])

for s in range(10):
  for a in range(10):
    for i in range(10):
      row = 10*s + i
      if row > 3:
        RandAddNode(randG[a],i)
        WeigthAddNode(weigthG[a],i)
        LengthAddNode(lengthG[a],i)
        randCC[a][row] = nx.average_clustering(randG[a])
        weigthCC[a][row] = nx.average_clustering(weigthG[a])
        lengthCC[a][row] = nx.average_clustering(lengthG[a])

rave = [0.0 for a in range(len(randCC[0]))]
wave = [0.0 for a in range(len(randCC[0]))]
lave = [0.0 for a in range(len(randCC[0]))]

for a in range(len(randCC[0])):
  for i in range(len(randCC)):
    rave[a] = (rave[a] + randCC[i][a])/10
    wave[a] = (wave[a] + weigthCC[i][a])/10
    lave[a] = (lave[a] + lengthCC[i][a])/10

embed()
