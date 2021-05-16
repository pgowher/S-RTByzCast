#!/usr/bin/python3

import sys
import random
import os
import subprocess
import pickle
import threading
import time
from matplotlib import pyplot as plt
import numpy as np
from ctypes import c_double
import os.path
import math

import networkx as nx

def printToFile(G, numNodes, numFaulty, pLoss, bNode, filename):
    adjtemp = nx.to_numpy_matrix(G)
    adjmat = adjtemp.astype(int)
    #print(adjmat)
    f= open(filename,"w")
    f.write(str(numNodes)+"\n")
    for n in range(numNodes):
        for m in range(numNodes):
            a= adjmat.item(n,m)
            f.write(str(a)+' ')
        f.write("\n")
    f.write("%i\n" % numFaulty)
    f.write("%f\n" % pLoss)
    f.write(str(bNode)+"\n")
    f.close()
    
def showGraph(G):
    nx.draw_networkx(G,with_labels=True)
    plt.show()

def fullyConnectedGraph(numNodes, numFaulty, pLoss, bNode):
    G = nx.Graph()
    #print('FULLY CONNECTED TOPOLOGY')
    for i in range(numNodes):
        G.add_node(i)
    for i in range(numNodes):
        for j in range(i+1,numNodes):
            G.add_edge(i,j)
    #showGraph(G)
    
    filename='generatedTopologies/topo_fully_'+str(numNodes)+'_'+str(numFaulty)+'_'+str(pLoss)+'_'+str(bNode)+'.txt'
    printToFile(G, numNodes, numFaulty, pLoss, bNode, filename)
    
    return G

def worstCaseGraph(numNodes, numFaulty, pLoss, bNode):
    G = nx.Graph()
    #print('WORST CASE TOPOLOGY')
    for i in range(numNodes):
        G.add_node(i)

    for i in range(numFaulty): # connect faulty nodes to all nodes
        for j in range(i+1, numNodes):
            G.add_edge(i, j)

    for i in range(numFaulty, numNodes-1): # single chain between correct nodes
        G.add_edge(i, i+1)
    
    #showGraph(G)
    
    filename='generatedTopologies/topo_worst_'+str(numNodes)+'_'+str(numFaulty)+'_'+str(pLoss)+'_'+str(bNode)+'.txt'
    printToFile(G, numNodes, numFaulty, pLoss, bNode, filename)
    return G

def randomGraph(numNodes, numFaulty, pLoss, bNode):
    doNewGraph = True
    #print('RANDOM TOPOLOGY')
    while doNewGraph: 
        G = nx.Graph()
        for i in range(numNodes):
            G.add_node(i)
            
        for i in range(numNodes):
            while len(list(nx.neighbors(G, i))) < numFaulty+1:
                available = list(nx.non_neighbors(G, i))
                if len(available) > 0:
                    j = available[random.randint(0, len(available)-1)]
                else:
                    notYetConnected = []
                    for j in range(numNodes):
                        if j != i and (not j in nx.neighbors(G, i)):
                            notYetConnected.append(j)
                    j = notYetConnected[random.randint(0, len(notYetConnected)-1)]

                G.add_edge(i, j)
        if nx.node_connectivity(G) == numFaulty + 1:
            doNewGraph = False
    #showGraph(G)
    
    filename='generatedTopologies/topo_random_'+str(numNodes)+'_'+str(numFaulty)+'_'+str(pLoss)+'_'+str(bNode)+'.txt'
    printToFile(G, numNodes, numFaulty, pLoss, bNode, filename)
    return G




#fullyConnectedGraph(7)
#randomGraph(7,2)
#worstCaseGraph(7, 3)
