# Barnch and Bound algorithm to solve Traveling Salesman problem

from queue import PriorityQueue

INF = float('inf')

class BNB:
    def __init__(self, matrix, weightInfo, adjList, adj):
        self.matrix = matrix
        self.weightInfo = weightInfo
        self.adjList = adjList
        self.adj = adj
        self.N = len(matrix)-1

    class Node:
        def __init__(   self, path=[], 
                        reducedMatrix=[], 
                        cost=None, 
                        vertex=None, 
                        level=None, 
                        effort=0, 
                        weight=0
                    ):

            self.path = path                    # list of tuples 
            self.reducedMatrix = reducedMatrix  # NxN array of integers
            self.cost = cost                    # integer -> lower bound cost
            self.vertex = vertex                # integer -> current city number
            self.level = level                  # integer -> number of cities visited so far
            self.effort = effort                # Integer -> amount of effort expended so far
            self.weight = weight

        def __lt__(self, o):
            return self.cost < o.cost

        def __gt__(self, o):
            return self.cost > o.cost

        def __eq__(self, o):
            return self.cost == o.cost


    def newNode(self, parentMatrix, path, level, i, j, e, w, N):
        node = self.Node()
        node.path = path

        if level != 0:
            node.path.append((i,j))
        
        node.reducedMatrix = parentMatrix
        k = 0
        while level != 0 and k < N:
            node.reducedMatrix[i][k] = INF
            node.reducedMatrix[k][j] = INF
            k += 1

        node.reducedMatrix[j][0] = INF
        node.level = level
        node.vertex = j
        node.effort = e
        node.weight = w
        
        return node


    def rowReduction(self, reducedMatrix, row, N) -> list:
        for i in range(N):
            for j in range(N):
                if reducedMatrix[i][j] < row[i]:
                    row[i] = reducedMatrix[i][j]
        
        for i in range(N):
            for j in range(N):
                if reducedMatrix[i][j] != INF and row[i] != INF:
                    reducedMatrix[i][j] -= row[i]



    def columnReduction(self, reducedMatrix, col, N) -> list:
        for i in range(N):
            for j in range(N):
                if reducedMatrix[i][j] < col[j]:
                    col[j] = reducedMatrix[i][j]
        
        for i in range(N):
            for j in range(N):
                if reducedMatrix[i][j] != INF and col[j] != INF:
                    reducedMatrix[i][j] -= col[j]



    def calculateCost(self, reducedMatrix, N) -> int:
        cost = 0

        row = [INF for i in range(N)]
        col = [INF for i in range(N)]
        
        self.rowReduction(reducedMatrix, row, N)
        self.columnReduction(reducedMatrix, col, N)

        for i in range(N):
            cost += (row[i] if row[i] != INF else 0)
            cost += (col[i] if col[i] != INF else 0)

        return cost


    def printPath(self, l):
        for i in range(len(l)):
            print(l[i][0], end='')
            print(" -> ", end='')
            print(l[i][1])


    def solve(self, costMatrix, N) -> int:
        pq = PriorityQueue()
        v = []
        currentLevel = 0

        root = self.newNode(costMatrix, v, 0, -1, 0, 0, 0, N)
        root.cost = self.calculateCost(root.reducedMatrix, N)
        pq.put(root)

        while (not pq.empty()):
            minNode = pq.get()
            i = minNode.vertex
            '''
            if minNode.level <= currentLevel:
                continue
            else
                currentLevel += 1
            '''
            if minNode.level == N-1:
                minNode.path.append((i,self.N))
                minNode.cost -= self.matrix[i][0]
                minNode.cost += self.matrix[i][self.N]

                effort = minNode.effort + (minNode.weight * self.adj[i][-1])

                minNode.path = minNode.path[1:]
                return minNode.cost, minNode.path, effort
            
            for j in range(N):
                if (minNode.reducedMatrix[i][j] != INF):                
                    reduced_tmp = [[x for x in y] for y in minNode.reducedMatrix]
                    path_tmp = minNode.path[:]
                    
                    child = self.newNode(reduced_tmp, path_tmp, minNode.level+1, i, j, minNode.effort, minNode.weight, N)
                    child.cost = minNode.cost + minNode.reducedMatrix[i][j] + self.calculateCost(child.reducedMatrix, N)
                    
                    child.effort = minNode.effort + (minNode.weight * self.adj[i][child.vertex])
                    child.weight += self.weightInfo[self.adjList[child.vertex]][3]
                    pq.put(child)
                    

    def print2DList(self, l):
        for i in l:
            for j in i:
                print('{:4}'.format(j), end='')
            print('\n')


    def optimalPath(self):
        tmp = [[x for x in y] for y in self.matrix]
        cost,path, effort = self.solve(tmp, self.N)
        path = [i[0] for i in path]

        return cost, path, effort


'''
def main():
    adj = [
        [ INF, 10,  8,   9,   7 ],
        [ 10,  INF, 10,  5,   6 ],
        [ 8,   10,  INF, 8,   9 ],
        [ 9,   5,   8,   INF, 6 ],
        [ 7,   6,   9,   6,   INF ]
    ]
    b = BNB(adj)
    c,d = b.optimalPath()
    print(c)
    print(d)

main()
'''


