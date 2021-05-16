/* C++-11: RANDOM TOPOLOGY WITH ALL NORMAL NODES
   /Program to simulate the multi-hop message broadcast in a network.
   / The program displays the probabilities of different nodes receiving a
   / broadcast packet after each round of broadcast. The simulation terminates
   / once each node has reached a 'Threshold" probability.
 */
#include <iostream>
#include <thread>         // std::this_thread::sleep_for
#include <chrono>
#include <fstream> 
#include <sstream>
#include <string>
#include <vector>
#include <time.h>
#include <set>
#include <math.h>

//#include "csvfile.h"      // CSV

using namespace std;

//initialize all the elements in probability matrix to '0'
void initWithZeros(double **s, int n) {
    for (int i = 0; i < n; i++) {
	for (int j = 0; j < n; j++) {
	    s[i][j] = 0.0;
	}
    }
}


//print all the elements in probability matrix
void printMatrix(double **s, int n) {
    for (int i = 0; i < n; i++) {
	for (int j = 0; j < n; j++) {
	    cout << s[i][j] << " ";
	}
	cout << endl;
    }
    cout << endl;
}

//check if all the elements in probability matrix have reached the 'Threshold'
bool correctNodesReceived(double **s, int n, int numFaults, bool *isFaulty) {
    double threshold = 0.9;
    for (int i = 0; i < n; i++) {
	if (isFaulty[i]) continue;
	int countSigns = 0;
	for (int j = 0; j < n; j++) {
	    if (s[i][j] >= threshold) {
		countSigns++;
	    }
	}
	if ((float) countSigns < ceil(float(n + numFaults + 1) / 2.0)) {
	    return false;
	}
    }
    return true;
}

//copy elements of probability matrix to a temporary matrix*
void copyMatrix(double **from, double **to,  int nrows, int ncols) {
    for (int i = 0; i < nrows; i++) {
	for (int j = 0; j < ncols; j++) {
	    to[i][j] = from[i][j];
	}
    }
}


int main(int argc, char** argv){

    ostringstream fileName;  
    fileName << argv[1];
    
    ifstream infile;
    infile.open(fileName.str());

    int numNodes=0;
    infile >> numNodes;
    cout << "Num nodes : " << numNodes << endl;


    //cout << "Adjacency matrix : " << endl;
    int **topo = new int *[numNodes];
    for (int i = 0; i < numNodes; i++) {
	topo[i] = new int[numNodes];
	for (int j = 0; j < numNodes; j++) {
	    infile >> topo[i][j];
            cout << topo[i][j] << " ";
	}
	cout << endl;
    }

    int numFaulty;
    infile >> numFaulty;
    cout <<"No. faulty nodes : " << numFaulty << endl;

    bool *isFaulty = new bool[numNodes];
    for (int i = 0; i < numFaulty; i++) {
	     isFaulty[i] = true;
    }
    for (int i = numFaulty; i < numNodes; i++) {
	isFaulty[i] = false;
    }

//    cout << "Faulty matrix:" <<endl;
//    for (int i = 0; i < numNodes; i++)
//    {
//        cout<<isFaulty[i]<< " ";
//    }
//    cout<<endl;

    float pLoss;
    infile >> pLoss;
    cout << "Packet loss probability: " << pLoss << endl;

    int bid;
    infile >> bid;
    cout << "Broadcast node ID: " << bid << endl;
    
    infile.close();
    
    double **s = new double*[numNodes]; 
    double **tmp = new double*[numNodes]; 

    //initialize the probability and temporary matrices
    for (int i=0; i < numNodes; i++) {
	s[i] = new double[numNodes];
	tmp[i] = new double[numNodes];
    }

    //initialize the probability and temporary matrices elements with '0'
    initWithZeros(s, numNodes);

    //set the broadcast start node
    s[bid][bid] = 1;

    int round = 0;
    while (!correctNodesReceived(s, numNodes, numFaulty, isFaulty)) {

	copyMatrix(s, tmp, numNodes, numNodes);

	for (int dst = 0; dst < numNodes; dst++) {
	    if (isFaulty[dst]) {
            	continue;
	    }

	    double probaAllFails = 1.0;
	    double probaMissSignFrom[numNodes];
	    for (int i = 0; i < numNodes; i++) {
		probaMissSignFrom[i] = 1.0;
	    }

	    for (int src = 0; src < numNodes; src++) {
		if (topo[src][dst] != 0 && !isFaulty[src]) {
                    probaAllFails *= (1-s[src][src]) + s[src][src]*pLoss; // either the src doesn't have the message, or it is lost

                    for (int i=0; i < numNodes; i++) {
                        probaMissSignFrom[i] *= (1-s[src][i]) + s[src][i]*pLoss; // either the src doesn't have the i's sign, or the msg is lost
                    }
                }
	    }

	    tmp[dst][dst] = s[dst][dst] + (1-s[dst][dst])*(1-probaAllFails);
            
	    for (int i = 0; i < numNodes; i++) {
		if (i != dst) {
                    tmp[dst][i] = s[dst][i] + (1-s[dst][i]) * (1-probaMissSignFrom[i]);
                }
	    }
	}
	
	copyMatrix(tmp, s, numNodes, numNodes);

	printMatrix(s, numNodes);
        
// 	std::this_thread::sleep_for (std::chrono::seconds(10));
	round+=1;
    }

    cout << "Total number of rounds: " << round << endl;

    for (int i=0; i < numNodes; i++) {
	delete[] s[i];
	delete[] tmp[i];
    }
    delete[] s;
    delete[] tmp;
    
    delete[] isFaulty;

    return 0;
}
