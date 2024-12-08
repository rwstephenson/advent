class Point:

    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.maxX = len(grid[0]) - 1
        self.maxY = len(grid) - 1
        self.grid = grid

    def __str__(self):
        return "Point({0},{1})".format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y,self.grid)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y,self.grid)

    def __hash__(self):
        return hash((self.x, self.y))

    def isOutside(self):
        return self.x < 0 or self.x > self.maxX or self.y < 0 or self.y > self.maxY

    def isInside(self):
        return not self.isOutside()

    def getValue(self):
        if self.isInside():
            return self.grid[self.y][self.x]
        else:
            return None

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
        dirs = ['N','S','E','W']
        if diagonally:
            dirs += ['NE','SE','NW','SW']
        neighboors = [i for i in list(map(self.getNeighboor,dirs)) if i is not None]
        return neighboors

