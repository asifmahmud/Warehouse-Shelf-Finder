from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

class MST:
    def __init__(self, G):
        self.G = G

    def findMST(self):
        X = csr_matrix(self.G)
        Tcsr = minimum_spanning_tree(X)
        return Tcsr.toarray().astype(int)


class LowerBound:
    def __init__(self, G, start):
        self.G = G
        self.start = start

    def findLowerBound(self):
        mst = MST(self.G).findMST()

    def removeStart(self, arr, start):
        #TODO: Modify the 2D array to remove the start node
        pass

                
