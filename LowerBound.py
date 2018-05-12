
INF = float('inf')

class LowerBound:
    def __init__(self, matrix):
        self.matrix = [[x for x in y] for y in matrix]
        self.N = len(matrix)-1
        
    def rowReduction(self, row, N):
        for i in range(N):
            for j in range(N):
                if self.matrix[i][j] < row[i]:
                    row[i] = self.matrix[i][j]
        
        for i in range(N):
            for j in range(N):
                if self.matrix[i][j] != INF and row[i] != INF:
                    self.matrix[i][j] -= row[i]

    def columnReduction(self, col, N):
        for i in range(N):
            for j in range(N):
                if self.matrix[i][j] < col[j]:
                    col[j] = self.matrix[i][j]
        
        for i in range(N):
            for j in range(N):
                if self.matrix[i][j] != INF and col[j] != INF:
                    self.matrix[i][j] -= col[j]

    def lbound(self):
        cost = 0
        N = self.N

        row = [INF for i in range(N)]
        col = [INF for i in range(N)]
        
        self.rowReduction(row, N)
        self.columnReduction(col, N)

        for i in range(N):
            cost += (row[i] if row[i] != INF else 0)
            cost += (col[i] if col[i] != INF else 0)

        return cost

                
