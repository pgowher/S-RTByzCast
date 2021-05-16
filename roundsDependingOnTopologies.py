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

import generateTopos


# create a color palette
palette = plt.get_cmap('Set1')


ax1 = 0
fig = 0

SMALL_SIZE = 16
MEDIUM_SIZE = 16
BIGGER_SIZE = 16

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # deletefontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def create_fig(title, x_axis_label, y_axis_label):
    global fig, ax1
    a= 8
    fig = plt.figure()#figsize=(2*a+a/1.62,a))
    fig.set_size_inches(10, 6)
    ax1 = fig.add_subplot(111)
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.title(title)

def print_fig(fig_name):
    global fig, ax1
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    lgd = ax1.legend(borderaxespad=1.,fancybox=True,shadow=False,loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(fig_name, dpi=200)#, bbox_extra_artists=(lgd,), bbox_inches='tight')
    print("created output", fig_name)
    plt.close()

def jd_print_fig(fig_name):
    plt.savefig(fig_name, format='pdf', bbox_inches='tight')#, bbox_extra_artists=(lgd,), bbox_inches='tight')
    print("created output", fig_name)
    plt.close()

def avg_list(l):
    sum = 0.0
    for x in l:
        sum += float(x)
    return sum / float(len(l))

output_directory = './'
points = ["D", "o", "v", "s"]
lines = ["-", "--", "-.", ":"]
colors = ['red', 'black', 'blue', 'green']

itrange = range(0,3,1) # iteration id
nrange = range(10,101,10) # number of nodes
frange = range(1,33,1)  # number of faulty nodes
prange = [50] #[x for x in range(10,100,10)] # proba of msg loss
for i in range(len(prange)):
    prange[i] /= 100.0
    
res_fully = {}
res_random = {}
res_worst = {}
lastLine_fully = []
lastLine_random = []
lastLine_worst = []

if os.path.isfile('res_fully'):
    inf = open("res_fully", "rb")
    res_fully = pickle.load(inf)
    inf.close()

if os.path.isfile('res_random'):
    inf = open("res_random", "rb")
    res_random = pickle.load(inf)
    inf.close()

if os.path.isfile('res_worst'):
    inf = open("res_worst", "rb")
    res_worst = pickle.load(inf)
    inf.close()
    
def runExperiment(experiment):
    itrange = range(experiment[0])
    nrange = experiment[1]
    frange = experiment[2]
    prange = experiment[3]
    nbid = experiment[4]

    #cmd1 = subprocess.run('./initAndCompile.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for f in frange:

        #print("\t\tRUNNING WITH f =",f)
        
        if not f in res_fully:
            res_fully[f] = {}
            res_random[f] = {}
            res_worst[f] = {}

        for n in nrange:
            if f > int((33/100)*n):
                continue;
            if not n in res_fully[f]:
                res_fully[f][n] = {}
                res_random[f][n] = {}
                res_worst[f][n] = {}
            print("\t\tRUNNING WITH f =",f)
            num = n
            mid = int((f + num-1) / 2 )
            if nbid==1:
                brange = [f]
            elif nbid==2:
                brange = [f, num-1]
            else:
                brange = [f, mid, num-1]

            for pl in prange:

                if not pl in res_fully[f][n]:
                    res_fully[f][n][pl] = {}
                    res_random[f][n][pl] = {}
                    res_worst[f][n][pl] = {}
                
                for bid in brange:        

                    if (f in res_fully) and (n in res_fully[f]) and (bid in res_fully[f][n]) and (bid in res_fully[f][n][pl]):
                        continue
                    else:
                        res_fully[f][n][pl][bid] = []
                        res_random[f][n][pl][bid] = []
                        res_worst[f][n][pl][bid] = []
                    print('###################################################################')
                    print('Generating Topology '+str(num)+' '+str(f)+' '+str(pl)+' '+str(bid))
                    #cmd1 = subprocess.run('./exec_topogen '+str(num)+' '+str(f)+' '+str(pl)+' '+str(bid), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    for i in itrange:
                        print('Iteration:'+str(i))
                        # Generate the topologies for these parameters

                        generateTopos.fullyConnectedGraph(num, f, pl, bid)
                        generateTopos.randomGraph(num, f, pl, bid)
                        generateTopos.worstCaseGraph(num, f, pl, bid)
                        
                        # Compute the number of rounds required
                        print('Calculating number of rounds for: topo_fully_'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'.txt')
                        cmd2 = subprocess.run('./exec_computeRoundsProba ./generatedTopologies/topo_fully_'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'.txt > output/output_fully.'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'_'+str(i)+'.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                        print('Calculating number of rounds for: topo_random_'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'.txt')
                        cmd2 = subprocess.run('./exec_computeRoundsProba ./generatedTopologies/topo_random_'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'.txt > output/output_random.'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'_'+str(i)+'.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
                        print('Calculating number of rounds for: topo_worst_'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'.txt')
                        cmd2 = subprocess.run('./exec_computeRoundsProba ./generatedTopologies/topo_worst_'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'.txt > output/output_worst.'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'_'+str(i)+'.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
                        #sys.exit()
            
                        # Read the results in the output files
                        fname = 'output/output_fully.'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'_'+str(i)+'.txt'
                        inf = open(fname, 'r')
                        lastline = ''
                        for line in inf:
                            lastline = line
                        #print(lastline,end='')
                        inf.close()
                        lastLine_fully.append(int(lastline.split(':')[1]))



                        fname = 'output/output_random.'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'_'+str(i)+'.txt'
                        inf = open(fname, 'r')
                        lastline = ''
                        for line in inf:
                            lastline = line
                        #print(lastline,end='')
                        inf.close()
                        lastLine_random.append(int(lastline.split(':')[1]))

                        fname = 'output/output_worst.'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'_'+str(i)+'.txt'
                        inf = open(fname, 'r')
                        lastline = ''
                        for line in inf:
                            lastline = line

                        inf.close()
                        lastLine_worst.append(int(lastline.split(':')[1]))

                         # Remove the generated topologies
                        cmd2 = subprocess.run('rm ./generatedTopologies/topo_fully_'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        cmd2 = subprocess.run('rm ./generatedTopologies/topo_random_'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        cmd2 = subprocess.run('rm ./generatedTopologies/topo_worst_'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        
                        # Remove the output files
                        cmd2 = subprocess.run('rm ./output/output_fully.'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'_'+str(i)+'.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        cmd2 = subprocess.run('rm ./output/output_random.'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'_'+str(i)+'.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        cmd2 = subprocess.run('rm ./output/output_worst.'+str(num)+'_'+str(f)+'_'+str(pl)+'_'+str(bid)+'_'+str(i)+'.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    print(lastLine_fully)
                    print(lastLine_random)
                    print(lastLine_worst)

                    average= avg_list(lastLine_fully)
                    res_fully[f][n][pl][bid].append(round(average,2))

                    average= avg_list(lastLine_random)
                    res_random[f][n][pl][bid].append(round(average,2))

                    average= avg_list(lastLine_worst)
                    res_worst[f][n][pl][bid].append(round(average,2))

                    lastLine_fully.clear()
                    lastLine_random.clear()
                    lastLine_worst.clear()

                    outf = open("res_fully", "wb")
                    pickle.dump(res_fully, outf)
                    outf.close()

                    outf = open("res_random", "wb")
                    pickle.dump(res_random, outf)
                    outf.close()
                    
                    outf = open("res_worst", "wb")
                    pickle.dump(res_worst, outf)
                    outf.close()

# #iterations, nrange, frange, prange, nbid
experiment1 = [1, range(10,101,10), range(1, int(100/3)+1), [0.0, 0.2, 0.4, 0.6, 0.8, 0.9], 1]
runExperiment(experiment1)
