#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import random

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

#初期状態の生成
node = 8
seconds = 6000
case = 1

#関数

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
  alldegree = float()
  for i in degreeitem:
    alldegree = alldegree + float(i[1])
  for a in degreeitem:
    C.append((a[0],float(a[1])/alldegree))
  return random_weight_choice(C)

def LengthSelection(G,node):
  lengthdict = nx.single_source_dijkstra_path_length(G,str(node))
  flag = []
  for a in lengthdict.keys():
    neigh = G.neighbors(str(node))
    flag.append(a in neigh)
  if True in neigh:
    G.add_edge(str(i),str(LengthSelection(G,str(i))))
    C = []
    lengthitem = Lengthdict.items()
    allLength = float()
    for a in lengthitem:
      allLength = allLength + float(a[1])
    for a in lengthitem:
      C.append((a[0],float(a[1])/allLength))
    return random_weight_choice(C)
  else:
    return BasicSelection(G)

def RandAddEdge(G,flag,time,wait):
  #エッジ作成終了処理
  for n in range(node):
    #発行中であれば
    if flag.count(n) is not 0:
      #作成時間が残り0より長ければ
      if time[n] > 0:
        #時間を進める
        time[n] = time[n] - 1
      else:
        #作成を終了
        flag.remove(n)
  #エッジ作成してないものへの処理
  for a in range(node):
    if flag.count(a) is 0:
      target = a
      #作成を開始
      while True:
        #相手を乱択
        pair = random.randint(0,node-1)
        #pair = int(BasicSelection(G))
        if flag.count(pair) is 0 and pair is not target:
          break
      if pair is not wait[target][0]:
        G.add_edge(str(i),str(pair))
        maket = int(random.gauss(300,120))
        time[target] = maket
        time[pair] = maket
        wait[target] = [pair,maket+300]
        wait[pair] = [target,maket+300]
        flag.append(target)
        flag.append(pair)
      else:
        wait[target][1] = wait[target][1] - 1
        if wait[target][1] is 0:
          wait[target] = [None,None]

def DegAddEdge(G,flag,time,wait):
  #エッジ作成終了処理
  for n in range(node):
    #発行中であれば
    if flag.count(n) is not 0:
      #作成時間が残り0より長ければ
      if time[n] > 0:
        #時間を進める
        time[n] = time[n] - 1
      else:
        #作成を終了
        flag.remove(n)
  #エッジ作成してないものへの処理
  for a in range(node):
    if flag.count(a) is 0:
      target = a
      #作成を開始
      while True:
        #相手を次数で重み付けして乱択
        pair = int(BasicSelection(G))
        if flag.count(pair) is 0 and pair is not target:
          break
      if pair is not wait[target][0]:
        G.add_edge(str(i),str(pair))
        maket = int(random.gauss(300,120))
        time[target] = maket
        time[pair] = maket
        wait[target] = [pair,maket+300]
        wait[pair] = [target,maket+300]
        flag.append(target)
        flag.append(pair)
      else:
        wait[target][1] = wait[target][1] - 1
        if wait[target][1] is 0:
          wait[target] = [None,None]


def LengthAddEdge(G,flag,time,wait):
  #エッジ作成終了処理
  for n in range(node):
    #発行中であれば
    if flag.count(n) is not 0:
      #作成時間が残り0より長ければ
      if time[n] > 0:
        #時間を進める
        time[n] = time[n] - 1
      else:
        #作成を終了
        flag.remove(n)
  #エッジ作成してないものへの処理
  for a in range(node):
    if flag.count(a) is 0:
      target = a
      #作成を開始
      while True:
        #相手をパス距離で重み付けして乱択
        pair = int(LengthSelection(G,target))
        if flag.count(pair) is 0 and pair is not target:
          break
      if pair is not wait[target][0]:
        G.add_edge(str(i),str(pair))
        maket = int(random.gauss(300,120))
        time[target] = maket
        time[pair] = maket
        wait[target] = [pair,maket+300]
        wait[pair] = [target,maket+300]
        flag.append(target)
        flag.append(pair)
      else:
        wait[target][1] = wait[target][1] - 1
        if wait[target][1] is 0:
          wait[target] = [None,None]

def sort(map):
  ms=sorted(map.iteritems(), key=lambda (k,v): (-v,k))
  return ms

def makegraph(lave,wave,rave):
  plt.plot(lave,color="green",label="Make edge by length")
  plt.plot(wave,color="blue",label="Make edge by degree")
  plt.plot(rave,color="red",label="Make edge at random")
  plt.xlabel('Second')
  plt.ylabel('Clustering Coefficient')
  plt.legend(loc='upper left')


randG = [nx.Graph() for a in range(case)]
weigthG = [nx.Graph() for a in range(case)]
lengthG = [nx.Graph() for a in range(case)]

randCC = [None for a in range(len(randG))]
weigthCC = [None for a in range(len(weigthG))]
lengthCC = [None for a in range(len(lengthG))]

#発行中フラッグ
#発行中のものがぶち込まれる
rflag = [[] for a in range(case)]
wflag = [[] for a in range(case)]
lflag = [[] for a in range(case)]
#発行残り時間
rtime = [[0 for i in range(node)] for a in range(case)]
wtime = [[0 for i in range(node)] for a in range(case)]
ltime = [[0 for i in range(node)] for a in range(case)]
#待機時間
rwait = [{i:[None,None] for i in range(node)} for a in range(case)]
wwait = [{i:[None,None] for i in range(node)} for a in range(case)]
lwait = [{i:[None,None] for i in range(node)} for a in range(case)]


#初期状態生成
for a in range(len(randG)):
  for i in range(0,node-1,2):
    randG[a].add_edges_from([(str(i),str(i+1))])
    weigthG[a].add_edges_from([(str(i),str(i+1))])
    lengthG[a].add_edges_from([(str(i),str(i+1))])

  randCC[a] = [0.0 for row in range(seconds)]
  weigthCC[a] = [0.0 for row in range(seconds)]
  lengthCC[a] = [0.0 for row in range(seconds)]


#秒数を進める
for s in range(seconds):
  print "now making graph at "+str(s)+" second"
  for c in range(case):
    LengthAddEdge(lengthG[c],lflag[c],ltime[c],lwait[c])
    RandAddEdge(randG[c],rflag[c],rtime[c],rwait[c])
    DegAddEdge(weigthG[c],wflag[c],wtime[c],wwait[c])
    randCC[c][s] = nx.average_clustering(randG[c])
    weigthCC[c][s] = nx.average_clustering(weigthG[c])
    lengthCC[c][s] = nx.average_clustering(lengthG[c])

#データをマージ
rave = [0.0 for a in range(len(randCC[0]))]
wave = [0.0 for a in range(len(randCC[0]))]
lave = [0.0 for a in range(len(randCC[0]))]

for a in range(len(randCC[0])):
  for i in range(len(randCC)):
    rave[a] = (rave[a] + randCC[i][a])/len(randG)
    wave[a] = (wave[a] + weigthCC[i][a])/len(weigthG)
    lave[a] = (lave[a] + lengthCC[i][a])/len(lengthG)

makegraph(lave,wave,rave)
embed()
