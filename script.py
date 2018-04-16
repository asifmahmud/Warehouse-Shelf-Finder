
'''
------------------------------------
University of California, Irvine
EECS 221: Adv. App Algorithms

Author: Asif Mahmud
Date: 04/07/2018
Updated: 04/15/2018
------------------------------------
'''


import sys
import random
import queue

class ShelfFinder:
    def __init__(self, startLocation, endLocation, orderFile=None, outFile=None):
        self.warehouse  = 'warehouse-grid.csv'
        self.start      = startLocation
        self.end        = endLocation
        self.distance   = 0
        self.orderFile  = orderFile 
        self.outFile    = outFile
        self.orderBook  = dict()
        
        self.xMax, self.yMax = self._findRange()
        self.grid  = [[0 for x in range(self.xMax+2)] for y in range(self.yMax+2)]
        with open(self.warehouse) as w:
            line = w.readline().strip('\n').split(',')
            while(len(line) > 1):
                # Use integer coordinates for now
                k, i, j = int(float(line[0])), int(float(line[2])), int(float(line[1]))
                self.orderBook[k] = (i*2,j*2)
                self.grid[i*2][j*2] = 1
                line = w.readline().strip('\n').split(',')

    
    def optimumOrder(self, order):
        dist = dict()
        originDist = {0: []}
        optimizedOrder = []
        # Using brute force approach for now
        for i in order:
            x, y = self.findRoute(self.start, self.orderBook[i])
            originDist[0].append( (i, x, y) )
            
            for j in order:
                if i != j:
                    a, b = self.findRoute(self.orderBook[i], self.orderBook[j])
                    if i not in dist.keys():
                        dist[i] = [(j, a, b)]
                    else:
                        dist[i].append((j, a, b))
        

        (item, totalDist, loc) = self.findMinDistance(originDist[0])
        optimizedOrder.append(item)
        prevItem = item
        '''
        print(order)
        print(originDist)
        print(dist)
        '''
        for i in range(len(dist.keys()) - 1):
            (item, d, loc) = self.findMinDistance(dist[prevItem])
            while(item in optimizedOrder):
                #print(optimizedOrder)
                #print("Old item: {}".format(item))
                (item, d, loc) = self.findMinDistance(dist[prevItem], duplicate=item)
                #print("New Item: {}".format(item))
            prevItem = item
            totalDist += d
            optimizedOrder.append(item)
        '''
        print("===========================")
        print(dist)
        print("===========================")
        print(optimizedOrder)
        '''
    
        totalDist += self.findRoute(loc, self.end)[0] + 1
        return optimizedOrder, totalDist


    def findMinDistance(self, itemList, duplicate=None):
        minVal = float("inf")
        result = tuple()
        
        if (duplicate != None):
            for v in itemList:
                if v[0] == duplicate: 
                    itemList.remove(v)
        
        for v in itemList:
            if v[1] < minVal: 
                result = v
                minVal = v[1]
        return result


    def originalDistance(self, order):
        totalDist = 0
        start = self.start
        for i in order:
            (dist, loc) = self.findRoute(start, self.orderBook[i])
            totalDist += dist
            start = loc
        totalDist += self.findRoute(start, self.end)[0] + 1
        return totalDist


    def batchOrder(self, customOrder=None):
        orderNo = 1
        outFile = open(self.outFile, 'w')

        if (customOrder):
            opt, dist = self.optimumOrder(customOrder)
            print("Here is your optimal picking order:")
            print(",".join([str(i) for i in opt]))
            return

        with open(self.orderFile) as orderFile:
            line = orderFile.readline().strip().split('\t')
            try:
                while( len(line) >= 1 ):
                    order = [int(i) for i in line]
                    originalDist = self.originalDistance(order)
                    optimalOrder, optimalDist = self.optimumOrder(order)
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
                    outFile.write("\n\n\n\n---------------------------------------------------------\n")
                    orderNo += 1
                    line = orderFile.readline().strip().split('\t')
            
            except ValueError:
                print("Done!")


    class QItem:
        def __init__(self, row, col, dist):
            self.row = row
            self.col = col
            self.dist = dist


    def findRoute(self, start, end):
        source = self.QItem(start[0], start[1], 0)
        visited = [[0 for x in range(self.xMax+2)] for y in range(self.yMax+2)]

        for i in range(self.yMax+2):
            for j in range(self.xMax+2):
                if (self.grid[i][j] == 1):
                    visited[i][j] = True
                else:
                    visited[i][j] = False
        
        q = queue.Queue()
        q.put(source)
        visited[source.row][source.col] = True
        while (not q.empty()):
            p = q.get()

            if ((p.row, p.col) == (end[0]-1, end[1]) or 
                (p.row, p.col) == (end[0]+1, end[1])):
                #print("Distance is: {}, Item at: {}".format(p.dist+1, end))
                return p.dist, (p.row, p.col)
            
            if (p.row - 1 >= 0 and visited[p.row - 1][p.col] == False):
                q.put(self.QItem(p.row-1, p.col, p.dist + 1))
                visited[p.row-1][p.col] = True

            if (p.row + 1 < self.yMax+2 and visited[p.row + 1][p.col] == False):
                q.put(self.QItem(p.row + 1, p.col, p.dist + 1))
                visited[p.row + 1][p.col] = True
    
            if (p.col - 1 >= 0 and visited[p.row][p.col - 1] == False):
                q.put(self.QItem(p.row, p.col - 1, p.dist + 1))
                visited[p.row][p.col - 1] = True
            
            if (p.col + 1 < self.xMax+2 and visited[p.row][p.col + 1] == False):
                q.put(self.QItem(p.row, p.col + 1, p.dist + 1))
                visited[p.row][p.col + 1] = True
        
        print("Distance is: {}".format(-1))
        return -1, None



    def printStats(self, distance):
        self.printGrid()
        print("Item found!")
        print("Distance traveled: {}".format(distance))
        

    # Find the range of x and y-coordinates
    def _findRange(self):
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


def main(argv):
    startLocation   = input("Hello user, where is your worker?: ")
    endLocation     = input("Where is your worker's end location?: ")
    order           = input("What items would you like to pick?: ")
    orderFile       = input("Please list file of orders to be processed: ")
    orderOutputFile = input("Please list output file: ")

    startLocation = startLocation.strip("()").split(",")
    startLocation = (int(startLocation[0]), int(startLocation[1]))
    endLocation = endLocation.strip("()").split(",")
    endLocation = (int(endLocation[0]), int(endLocation[1]))
    order = [int(i) for i in order.strip().split(",")]
    
    finder = ShelfFinder(startLocation, endLocation, orderFile, orderOutputFile)
    #finder.optimumOrder(order)
    print("Please wait.....")
    if len(order) > 0:
        finder.batchOrder(order)
    finder.batchOrder()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
