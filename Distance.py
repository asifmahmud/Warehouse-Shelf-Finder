import queue

class QItem:
    def __init__(self, row, col, dist, prevPath):
        self.row = row
        self.col = col
        self.dist = dist
        self.path = prevPath[:]
        self.path.append((row,col))


class Distance:
    def __init__(self, xMax, yMax, grid):
        self.xMax   = xMax + 2
        self.yMax   = yMax + 2
        self.grid   = grid

    def findRoute(self, start, end):
        if (start == end): return 0, start, []

        source = QItem(start[0], start[1], 0, [])
        visited = [[0 for x in range(self.xMax)] for y in range(self.yMax)]

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

            if ((p.row, p.col) == (end[0]-1, end[1]) or 
                (p.row, p.col) == (end[0]+1, end[1])):
                return p.dist, (p.row, p.col), p.path
            
            if (p.row - 1 >= 0 and visited[p.row - 1][p.col] == False):
                q.put(QItem(p.row-1, p.col, p.dist + 1, p.path))
                visited[p.row-1][p.col] = True

            if (p.row + 1 < self.yMax and visited[p.row + 1][p.col] == False):
                q.put(QItem(p.row + 1, p.col, p.dist + 1, p.path))
                visited[p.row + 1][p.col] = True

            if (p.col - 1 >= 0 and visited[p.row][p.col - 1] == False):
                q.put(QItem(p.row, p.col - 1, p.dist + 1, p.path))
                visited[p.row][p.col - 1] = True
            
            if (p.col + 1 < self.xMax and visited[p.row][p.col + 1] == False):
                q.put(QItem(p.row, p.col + 1, p.dist + 1, p.path))
                visited[p.row][p.col + 1] = True
        
        return -1, None, None