#!/bin/bash

mkdir -p generatedTopologies

#g++ -std=c++11 -o exec_topogen topogen.cpp

g++ -std=c++11 -o exec_computeRoundsProba computeRoundsProba.cpp

mkdir -p output
