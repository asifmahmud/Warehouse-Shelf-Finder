'''
------------------------------------
Author: Asif Mahmud
Date: 04/07/2018
Updated: 05/19/2018
------------------------------------
'''

from Distance import Distance
from NearestNeighbor import NearestNeighbor
from BNB import BNB
from LowerBound import LowerBound

import numpy as np
import itertools
import sys
import time

INF = float("inf")
THRESHOLD = 19

class ShelfFinder:
    def __init__(self, startLoc, endLoc, alg, orderFile=None, outFile=None, weightFlag=False):
        self.warehouse  = 'warehouse-grid.csv'
        self.itemInfo   = 'item-dimensions-tabbed.txt'
        self.start      = startLoc
        self.end        = endLoc
        self.orderFile  = orderFile 
        self.outFile    = outFile
        self.orderBook  = {0: self.start, -1: self.end}
        self.weightInfo = {0: (0,0,0,0), -1: (0,0,0,0)}
        self.algorithm  = alg
        self.weightFlag = weightFlag
        
        self.xMax,self.yMax = self.findRange()
        self.grid           = [[0 for x in range(self.xMax+2)] for y in range(self.yMax+2)]
        
        self.invalidItem = False
        
        
        with open(self.warehouse) as w:
            line = w.readline().strip('\n').split(',')
            while(len(line) > 1):
                # Use integer coordinates for now
                k, i, j = int(float(line[0])), int(float(line[2])), int(float(line[1]))
                self.orderBook[k] = (i*2,j*2)
                self.grid[i*2][j*2] = 1
                line = w.readline().strip('\n').split(',')
        

        with open(self.itemInfo) as f:
            next(f)
            line = f.readline().strip('\n').split('\t')
            while(len(line) > 1):
                k, i, j, l, m = (   int(float(line[0])), 
                                    float(line[2]), 
                                    float(line[1]), 
                                    float(line[3]), 
                                    float(line[4])
                                )

                self.weightInfo[k] = (i, j, l, m)
                line = f.readline().strip('\n').split('\t')



    def optimizedOrder(self, order):
        self.checkInvalid(order)

        # Remove duplicates from order
        order = list(dict.fromkeys(order)) 

        # Corner Case
        if len(order) == 0:
            return []

        order       = [0] + order + [-1]
        numNodes    = len(order)
        adj         = [[0 for i in range(numNodes)] for j in range(numNodes)]
        adjList     = {}
        d           = Distance(self.xMax, self.yMax, self.grid)

        for i,j in enumerate(order): 
            adjList[i] = j

        
        for i,x in enumerate(order):
            for j,y in enumerate(order):
                if x == y:  
                    adj[i][j] = INF
                else:
                    adj[i][j] = d.findRoute(self.orderBook[x], self.orderBook[y])[0]



        # Calculate the original cost and effort
        origCost, origEffort = 0, 0
        weight = 0
        for i in range(len(adj)-1):
            origCost += adj[i][i+1]
            weight += self.weightInfo[adjList[i]][3]
            origEffort += weight * adj[i][i+1]
        

        # Calculate lower bound
        #lowerBound = LowerBound(adj).lbound()
        #print("lower bound: {}".format(lowerBound))

        #---------------------------------------#
        #           Branch and Bound            #
        #---------------------------------------#
        if self.algorithm == 'bnb':
            b = BNB(adj, self.weightInfo, adjList, adj)
            cost,path,effort = b.optimalPath()


        #---------------------------------------#
        #           Nearest Neighbor            #
        #---------------------------------------#
        elif self.algorithm == 'nn': #elif len(order)-2 > THRESHOLD:
            n = NearestNeighbor(np.array(adj), self.weightInfo, adjList)
            cost,path,effort = n.findMinPath()

        
        #---------------------------------------#
        #               Held-Karp               #
        #---------------------------------------#
        else:
            cost,path = self.cost(adj)
            
            weight = 0
            effort = 0
            for i in range(len(path)-1):
                weight += self.weightInfo[adjList[path[i]]][3]
                effort += weight * adj[path[i]][path[i+1]]

            weight += self.weightInfo[adjList[path[-1]]][3]
            effort+= weight * adj[path[-1]][len(adj)-1]


        if self.invalidItem:
            print("Note: The effort output is missing some information")

        
        path = [adjList[i] for i in path]
        return [origCost, origEffort, cost, path, effort]



    def cost(self, dists):
        n = len(dists) - 1
        C = {}

        for k in range(1, n):
            C[(1 << k, k)] = (dists[0][k], 0)

        for subset_size in range(2, n):
            for subset in itertools.combinations(range(1, n), subset_size):
                bits = 0
                for bit in subset:
                    bits |= 1 << bit

                for k in subset:
                    prev = bits & ~(1 << k)

                    res = []
                    for m in subset:
                        if m == 0 or m == k:
                            continue
                        res.append((C[(prev, m)][0] + dists[m][k], m))
                    C[(bits, k)] = min(res)

        bits = (2**n - 1) - 1

        res = []
        for k in range(1, n):
            res.append((C[(bits, k)][0] + dists[k][n], k))
        opt, parent = min(res)


        path = []
        for i in range(n - 1):
            path.append(parent)
            new_bits = bits & ~(1 << parent)
            _, parent = C[(bits, parent)]
            bits = new_bits

        return opt, list(reversed(path))
            

                
    def print2DList(self, l):
        for i in l:
            for j in i:
                print('{:4}'.format(j), end='')
            print('\n')


    def batchOrder(self, customOrder=None):
<<<<<<< HEAD
=======
        orderNo = 1
        outFile = open(self.outFile, 'w')
        finder = []

>>>>>>> 5e01466926d9dca9dd05fe6dfd77dc839f167700
        if customOrder:
            finder = self.optimizedOrder(customOrder)
            print("Here is your optimal picking order:")
<<<<<<< HEAD
            print(",".join([str(i) for i in optimalOrder]))
        
        else:
            orderNo = 1
            outFile = open(self.outFile, 'w')

            with open(self.orderFile) as orderFile:
                line = orderFile.readline().strip().split('\t')
                try:
                    while( len(line) >= 1 ):
                        print("Processing Order #{}".format(orderNo))
                        order = [int(i) for i in line]
                        originalDist = self.originalDistance(order)
                        optimalDist, optimalOrder = self.optimizedOrder(order)
                        output = ''
=======
            print(",".join([str(i) for i in finder[3]]))
            return

        with open(self.orderFile) as orderFile:
            line = orderFile.readline().strip().split('\t')
            try:
                while( len(line) >= 1 ):
                    print("Processing Order Number {}".format(orderNo))
                    order = [int(i) for i in line]
                    t1 = time.time()
                    finder = self.optimizedOrder(order)
                    t2 = time.time()
                    
                    output = ''
                    if len(finder) == 0:
                        output += "Missing item information for this order\n"
                    
                    else:
>>>>>>> 5e01466926d9dca9dd05fe6dfd77dc839f167700
                        output += "##Order Number##\n"
                        output += str(orderNo) + '\n'
                        output += "##Worker Start Location##\n"
                        output += str(self.start) + '\n'
                        output += "##Worker End Location##\n"
                        output += str(self.end) + '\n'
                        output += "##Original Parts Order##\n"
                        output += ','.join([str(i) for i in order]) + '\n'
                        output += "##Optimized Parts Order##\n"
<<<<<<< HEAD
                        output += ','.join([str(i) for i in optimalOrder]) + '\n'
                        output += "##Original Parts Total Distance##\n"
                        output += str(originalDist) + '\n'
                        output += "##Optimized Parts Total Distance##\n"
                        output += str(optimalDist)

                        outFile.write(output)
                        outFile.write("\n\n---------------------------------------------------------\n\n")
                        orderNo += 1
                        line = orderFile.readline().strip().split('\t')
                
                except ValueError:
                    print("Done!")
=======
                        output += ','.join([str(i) for i in finder[3]]) + '\n'
                        output += "##Original Parts Total Distance##\n"
                        output += str(int(finder[0])) + '\n'
                        output += "##Optimized Parts Total Distance##\n"
                        output += str(int(finder[2])) + "\n"
                        output += str("Time taken: {}".format(t2-t1))

                        if (self.weightFlag):
                            output += "\n##Original Parts Total Effort##\n"
                            output += str(int(finder[1])) + "\n"
                            output += "##Optimal Parts Total Effort\n"
                            output += str(int(finder[4]))


                    outFile.write(output)
                    outFile.write("\n\n---------------------------------------------------------\n\n")
                    orderNo += 1
                    line = orderFile.readline().strip().split('\t')
            
            except ValueError:
                print("Done!")
                outFile.close()


    # Check invalid orders
    def checkInvalid(self, order):
        o = order[:]
        for i in o:
            try:
                a = self.weightInfo[i]
            except KeyError:
                self.invalidItem = True
                order.remove(i)
        return order
>>>>>>> 5e01466926d9dca9dd05fe6dfd77dc839f167700


    # Find the range of x and y-coordinates
    def findRange(self):
        xMax, yMax = 0, 0
        with open(self.warehouse) as w:
            line = w.readline().strip('\n').split(',')
            while(len(line) > 1):
                if int(float(line[1])) > xMax:
                    xMax = int(float(line[1]))
                if int(float(line[2])) > yMax:
                    yMax = int(float(line[2]))
                line = w.readline().strip('\n').split(',')
        
        return xMax * 2, yMax * 2


    # A string representation of the coordinate system
    def printGrid(self, c=None):
        if (not c):
            g = '\n' 
            for i in self.grid:
                for j in i:
                    g += ' . ' if j == 0 else ' x '
                g += '\n'
            print(g)
        else:       
            print(self.grid[c[1]][c[0]])
