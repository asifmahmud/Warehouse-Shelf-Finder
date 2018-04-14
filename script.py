
'''
------------------------------------
University of California, Irvine
EECS 221: Adv. App Algorithms

Author: Asif Mahmud
Date: 04/07/2018
Updated: 04/12/2018
------------------------------------
'''


import sys
import random
import queue

class ShelfFinder:
    def __init__(self, startLocation, endLocation, order=None, orderFile=None):
        self.warehouse  = 'warehouse-grid.csv'
        self.start      = startLocation
        self.end        = endLocation
        self.distance   = 0
        self.order      = order
        self.orderFile  = orderFile 
        self.orderBook  = dict()
        
        self.xMax, self.yMax = self._findRange()
        self.grid  = [[0 for x in range(self.xMax+1)] for y in range(self.yMax+1)]
        with open(self.warehouse) as w:
            line = w.readline().strip('\n').split(',')
            while(len(line) > 1):
                # Use integer coordinates for now
                k, i, j = int(float(line[0])), int(float(line[2])), int(float(line[1]))
                self.orderBook[k] = (i*2,j*2)
                self.grid[i*2][j*2] = 1
                line = w.readline().strip('\n').split(',')

    
    def optimumOrder(self):
        dist = dict()
        for order in self.order:
            dist[order] = (self.minDistance(self.start, self.orderBook[order]))
        print(dist)


    class QItem:
        def __init__(self, row, col, dist):
            self.row = row
            self.col = col
            self.dist = dist


    def minDistance(self, start, end):
        source = self.QItem(start[0], start[1], 0)
        visited = [[0 for x in range(self.xMax+1)] for y in range(self.yMax+1)]

        for i in range(self.yMax):
            for j in range(self.xMax):
                if (self.grid[i][j] == 1):
                    visited[i][j] = True
                else:
                    visited[i][j] = False
        
        q = queue.Queue()
        q.put(source)
        visited[source.row][source.col] = True
        while (not q.empty()):
            p = q.get()

            if ((p.row, p.col) == end):
                print("Distance is: {}".format(p.dist))
                return p.dist
            
            if (p.row - 1 >= 0 and visited[p.row - 1][p.col] == False):
                q.put(self.QItem(p.row-1, p.col, p.dist + 1))
                visited[p.row-1][p.col] = True

            if (p.row + 1 < self.yMax and visited[p.row + 1][p.col] == False):
                q.put(self.QItem(p.row + 1, p.col, p.dist + 1))
                visited[p.row + 1][p.col] = True
    
            if (p.col - 1 >= 0 and visited[p.row][p.col - 1] == False):
                q.put(self.QItem(p.row, p.col - 1, p.dist + 1))
                visited[p.row][p.col - 1] = True
            
            if (p.col + 1 < self.xMax and visited[p.row][p.col + 1] == False):
                q.put(self.QItem(p.row, p.col + 1, p.dist + 1))
                visited[p.row][p.col + 1] = True
        
        print("Distance is: {}".format(-1))
        return -1



    def printStats(self, distance):
        self.printGrid()
        print("Item found!")
        print("Distance traveled: {}".format(distance))
        

    # Find the range of the x and y-coordinates
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
    startLocation   = (4,9)
    endLocation     = (0, 18)
    order           = '444, 172, 360031, 1621964'
    orderFile       = 'warehouse-orders-v01.csv'
    #orderOutputFile = 'warehouse-orders-v01-optimized.csv'

    order = [int(i) for i in order.split(",")]

    finder = ShelfFinder(startLocation, endLocation, order, orderFile)
    finder.minDistance(startLocation, (10,15))
    #finder.optimumOrder()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
