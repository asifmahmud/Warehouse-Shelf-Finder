import numpy as np

class NearestNeighbor:
    def __init__(self, graph, weightInfo, adjList):
        self.graph = graph
        self.weightInfo = weightInfo
        self.adjList = adjList

    def NN(self, start):
        cutoff  = len(self.graph)-1
        A       = self.graph[:cutoff,:cutoff]

        path    = [start]
        cost    = 0
        effort  = 0 
        weight  = 0
        N       = A.shape[0]
        mask    = np.ones(N, dtype=bool)   # boolean values indicating which 
                                        # locations have not been visited
        mask[start] = False

        for i in range(N-1):
            last = path[-1]
            next_ind = np.argmin(A[last][mask])    # find minimum of remaining locations
            next_loc = np.arange(N)[mask][next_ind]         # convert to original location
            path.append(next_loc)
            mask[next_loc] = False
            cost += A[last, next_loc]
            
            weight += self.weightInfo[self.adjList[last]][3]
            if next_loc != 0:
                effort +=  weight * A[last, next_loc]
                    
        cost += self.graph[next_loc, cutoff] 
        effort += weight * self.graph[last, cutoff]

        return cost, path, effort


    def findMinPath(self):
        minPath, minCost, minEffort = [], float("inf"), float("inf")
        
        for i in range(len(self.graph)-1):
            cost,path,effort = self.NN(i)
            if cost < minCost:
                minCost,minPath, minEffort = cost,path,effort
        
        if minPath[0] != 0:
            res = []
            i = 0
            while i < len(minPath):
                if minPath[i] != 0:
                    res.append(minPath[i])
                    i += 1
                else:
                    minPath = minPath[i:] + res
                    break

        minPath = minPath[1:]
        return minCost, minPath, minEffort

'''
A = [
    [0, 2, 9, 2, 2],
    [2, 0, 2, 1, 1],
    [1, 2, 0, 1, 2],
    [2, 1, 1, 0, 2],
    [2, 1, 2, 2, 0]]

N = NearestNeighbor(np.array(A))
print(N.findMinPath())
'''