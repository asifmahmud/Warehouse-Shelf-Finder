
'''
------------------------------------
University of California, Irvine
EECS 221: Adv. App Algorithms

Author: Asif Mahmud
Date: 04/07/2018
Updated: 04/22/2018
------------------------------------
'''

from Distance import Distance
import itertools

class ShelfFinder:
    def __init__(self, startLoc, endLoc, orderFile=None, outFile=None):
        self.warehouse  = 'warehouse-grid.csv'
        self.start      = startLoc
        self.end        = endLoc
        self.orderFile  = orderFile 
        self.outFile    = outFile
        self.orderBook  = {}
        
        self.xMax,self.yMax = self.findRange()
        self.grid           = [[0 for x in range(self.xMax+2)] for y in range(self.yMax+2)]
        self.orderBook[0]   = self.start
        self.orderBook[-1]  = self.end
        
        with open(self.warehouse) as w:
            line = w.readline().strip('\n').split(',')
            while(len(line) > 1):
                # Use integer coordinates for now
                k, i, j = int(float(line[0])), int(float(line[2])), int(float(line[1]))
                self.orderBook[k] = (i*2,j*2)
                self.grid[i*2][j*2] = 1
                line = w.readline().strip('\n').split(',')


    def optimizedOrder(self, order):
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
                    adj[i][j] = 0
                else:       
                    adj[i][j] = d.findRoute(self.orderBook[x], self.orderBook[y])[0]

        cost,path = self.cost(adj)
        path = [adjList[i] for i in path]
        return cost,path


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


    def originalDistance(self, order):
        totalDist = 0
        start = self.start
        d = Distance(self.xMax, self.yMax, self.grid)
        
        for i in order:
            (dist, loc) = d.findRoute(start, self.orderBook[i])
            totalDist += dist
            start = loc

        totalDist += d.findRoute(start, self.end)[0] + 1
        return totalDist


    def batchOrder(self, customOrder=None):
        if customOrder:
            optimalDist, optimalOrder = self.optimizedOrder(customOrder)
            print("Here is your optimal picking order:")
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
                        output += "##Order Number##\n"
                        output += str(orderNo) + '\n'
                        output += "##Worker Start Location##\n"
                        output += str(self.start) + '\n'
                        output += "##Worker End Location##\n"
                        output += str(self.end) + '\n'
                        output += "##Original Parts Order##\n"
                        output += ','.join([str(i) for i in order]) + '\n'
                        output += "##Optimized Parts Order##\n"
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
