class Point:

    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.maxX = len(grid[0]) - 1
        self.maxY = len(grid) - 1
        self.grid = grid
        if self.x < 0 or self.x > self.maxX or self.y < 0 or self.y > self.maxY:
            self.value = None
        else:
            self.value = self.grid[self.y][self.x]

    def __str__(self):
        return "Point({0},{1})".format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y,self.grid)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y,self.grid)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self,other,cartesian=False):
        assert(not cartesian)
        return abs(self.x-other.x) + abs(self.y-other.y)

    def getNeighboor(self, d):
        if d == 'N' and self.y > 0:
            return Point(self.x, self.y - 1, self.grid)
        elif d == 'S' and self.y < self.maxY:
            return Point(self.x, self.y + 1, self.grid)
        elif d == 'W' and self.x > 0:
            return Point(self.x-1, self.y, self.grid)
        elif d == 'E' and self.x < self.maxX:
            return Point(self.x+1, self.y, self.grid)
        elif d == 'NW' and self.y > 0 and self.x > 0:
            return Point(self.x-1, self.y-1, self.grid)
        elif d == 'NE' and self.y > 0 and self.x < self.maxX:
            return Point(self.x+1, self.y-1, self.grid)
        elif d == 'SW' and self.y < self.maxY and self.x > 0:
            return Point(self.x-1, self.y+1, self.grid)
        elif d == 'SE' and self.y < self.maxY and self.x < self.maxX:
            return Point(self.x+1, self.y+1, self.grid)
        return None

    def getNeighboors(self, diagonally=False):
        dirs = ['E','W','N','S']
        if diagonally:
            dirs += ['NE','SE','NW','SW']
        neighboors = [i for i in list(map(self.getNeighboor,dirs)) if i is not None]
        return neighboors

    def bfs(self,other,exclusions):
        q = []
        seen = set()
        prev = {}
        q.append(self)
        prev[self] = None
        seen.add(self)
        while len(q) > 0:
            p = q.pop(0)
            for n in p.getNeighboors():
                if n.value not in exclusions and n not in seen:
                    q.append(n)
                    prev[n] = p
                    seen.add(n)
        path = []
        if other in seen:
            p = other
            path.append(other)
            while prev[p] is not None:
                p = prev[p]
                path.append(p)
            path.reverse()
        return path

    def find(self,value):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == value:
                    return Point(c,r,self.grid)
        return None

