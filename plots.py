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
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def create_fig(title, x_axis_label, y_axis_label):
    global fig, ax1
    a= 8
    fig = plt.figure()#figsize=(2*a+a/1.62,a))
    fig.set_size_inches(20, 12)
    ax1 = fig.add_subplot(111)
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.title(title)

    ax1.yaxis.get_ticklocs(minor=True)
    ax1.minorticks_on()
    ax1.xaxis.set_tick_params(which='minor', bottom=False)

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

iteration = 1
#nrange = range(3,20,1)
#frange = range(1,5,1)
#prange = [x for x in range(10,100,10)]
#for i in range(len(prange)):
   #prange[i] /= 100.0
    
res_fully = {}
res_random = {}
res_worst = {}

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

######################################################################
create_fig("Impact of faulty nodes on time/rounds", "Value of parameter f", "Number of rounds")

y_fully = []
y_random = []
y_worst = []
x = []

nrange = [100]
frange = range(1, int(100/3)+1)
prange = [0.9]

for f in frange:
    for n in nrange:
        for pl in prange:
            bid=f
            x.append(f)
            y_fully.append(avg_list(res_fully[f][n][pl][bid]))
            y_random.append(avg_list(res_random[f][n][pl][bid]))
            y_worst.append(avg_list(res_worst[f][n][pl][bid]))

plt.plot(x, y_fully, lines[0%len(lines)]+points[0%len(points)], color=palette(0), label='full, num='+str(nrange[0])+', pl='+str((prange[0])*100)+'%')
plt.plot(x, y_random, lines[1%len(lines)]+points[1%len(points)], color=palette(1), label='random, num='+str(nrange[0])+', pl='+str((prange[0])*100)+'%')
plt.plot(x, y_worst, lines[2%len(lines)]+points[2%len(points)], color=palette(2), label='worst, num='+str(nrange[0])+', pl='+str((prange[0])*100)+'%')

#my_xticks = [str(k) for k in range(0, 110, 10)]
#plt.xticks(np.arange(0, 110, 10)) #my_xticks) #range(len(mp)), ['10-6', '', '10-4', '', '10-2', '', '0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9'])
#plt.yticks([x/100.0 for x in np.arange(0, 110, 10)])
plt.legend()
plt.show()
#jd_print_fig('crash_proba_changing_X.pdf')

###############################################################
create_fig("Impact of message loss on time/rounds", "Proba of msg loss", "Number of rounds")

y_fully = []
y_random = []
y_worst = []
x = []


nrange = [100]
frange = [33]
prange = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9]
    
for f in frange:
    for n in nrange:
        for pl in prange:
            bid=f
            x.append(pl*100)
            y_fully.append(avg_list(res_fully[f][n][pl][bid]))
            y_random.append(avg_list(res_random[f][n][pl][bid]))
            y_worst.append(avg_list(res_worst[f][n][pl][bid]))

plt.plot(x, y_fully, lines[0%len(lines)]+points[0%len(points)], color=palette(0), label='full, num='+str(nrange[0])+', f='+str(frange[0])+'%')
plt.plot(x, y_random, lines[1%len(lines)]+points[1%len(points)], color=palette(1), label='random, num='+str(nrange[0])+', f='+str(frange[0])+'%')
plt.plot(x, y_worst, lines[2%len(lines)]+points[2%len(points)], color=palette(2), label='worst, num='+str(nrange[0])+', f='+str(frange[0])+'%')

#my_xticks = [str(k) for k in range(0, 110, 10)]
#plt.xticks(np.arange(0, 110, 10)) #my_xticks) #range(len(mp)), ['10-6', '', '10-4', '', '10-2', '', '0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9'])
#plt.yticks([x/100.0 for x in np.arange(0, 110, 10)])
plt.legend()
plt.show()

##################################################################
create_fig("Impact of number of nodes on time/rounds", "Number of nodes", "Number of rounds")

y_fully = []
y_random = []
y_worst = []
x = []

nrange = range(10,101,10)
frange = range(1, int(100/3)+1)
prange = [0.9]

for f in frange:
    for n in nrange:
        if f != int((33/100)*n):
            continue;
        for pl in prange:
            bid=f
            x.append(n)
            y_fully.append(avg_list(res_fully[f][n][pl][bid]))
            y_random.append(avg_list(res_random[f][n][pl][bid]))
            y_worst.append(avg_list(res_worst[f][n][pl][bid]))

plt.plot(x, y_fully, lines[0%len(lines)]+points[0%len(points)], color=palette(0), label='full, f='+str((33/100)*n)+'%, pl='+str((prange[0])*100)+'%')
plt.plot(x, y_random, lines[1%len(lines)]+points[1%len(points)], color=palette(1), label='random, f='+str((33/100)*n)+'%, pl='+str((prange[0])*100)+'%')
plt.plot(x, y_worst, lines[2%len(lines)]+points[2%len(points)], color=palette(2), label='worst, f='+str((33/100)*n)+'%, pl='+str((prange[0])*100)+'%')

###my_xticks = [str(k) for k in range(0, 110, 10)]
###plt.xticks(np.arange(0, 110, 10)) #my_xticks) #range(len(mp)), ['10-6', '', '10-4', '', '10-2', '', '0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9'])
###plt.yticks([x/100.0 for x in np.arange(0, 110, 10)])
plt.legend()
plt.show()

##################################################################
create_fig("Impact of number of nodes and message loss on time/rounds", "Number of nodes", "Number of rounds")

y_fully = []
y_random = []
y_worst = []
x = []

nrange = range(10,101,10)
frange = range(1, int(100/3)+1)
prange = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9]

for f in frange:
    for n in nrange:
        if f != int((33/100)*n):
            continue;
        for pl in prange:
            bid=f
            x.append(n)
            y_fully.append(avg_list(res_fully[f][n][pl][bid]))
            y_random.append(avg_list(res_random[f][n][pl][bid]))
            y_worst.append(avg_list(res_worst[f][n][pl][bid]))

plt.plot(x, y_fully, lines[0%len(lines)]+points[0%len(points)], color=palette(0), label='full, f='+str((33/100)*n)+'%')
plt.plot(x, y_random, lines[1%len(lines)]+points[1%len(points)], color=palette(1), label='random, f='+str((33/100)*n)+'%')
plt.plot(x, y_worst, lines[2%len(lines)]+points[2%len(points)], color=palette(2), label='worst, f='+str((33/100)*n)+'%')

###my_xticks = [str(k) for k in range(0, 110, 10)]
###plt.xticks(np.arange(0, 110, 10)) #my_xticks) #range(len(mp)), ['10-6', '', '10-4', '', '10-2', '', '0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9'])
###plt.yticks([x/100.0 for x in np.arange(0, 110, 10)])
plt.legend()
plt.show()

##################################################################
create_fig("Impact of number of nodes, faulty nodes and message loss on time/rounds", "Number of nodes", "Number of rounds")

y_fully = []
y_random = []
y_worst = []
x = []

nrange = range(10,101,10)
frange = range(1, int(100/3)+1,2)
prange = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9]

for f in frange:
    for n in nrange:
        if f > int((33/100)*n):
            continue;
        for pl in prange:
            bid=f
            x.append(n)
            y_fully.append(avg_list(res_fully[f][n][pl][bid]))
            y_random.append(avg_list(res_random[f][n][pl][bid]))
            y_worst.append(avg_list(res_worst[f][n][pl][bid]))

plt.plot(x, y_fully, lines[0%len(lines)]+points[0%len(points)], color=palette(0), label='full, f_Max='+str((33/100)*n)+'% (increases by 2%), pl=0% to 90% (increases by 20%)')
plt.plot(x, y_random, lines[1%len(lines)]+points[1%len(points)], color=palette(1), label='random, f_Max='+str((33/100)*n)+'% (increases by 2%), pl=0% to 90% (increases by 20%)')
plt.plot(x, y_worst, lines[2%len(lines)]+points[2%len(points)], color=palette(2), label='worst, f_Max='+str((33/100)*n)+'% (increases by 2%), pl=0% to 90% (increases by 20%)')

###my_xticks = [str(k) for k in range(0, 110, 10)]
###plt.xticks(np.arange(0, 110, 10)) #my_xticks) #range(len(mp)), ['10-6', '', '10-4', '', '10-2', '', '0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9'])
###plt.yticks([x/100.0 for x in np.arange(0, 110, 10)])
plt.legend()
plt.show()
