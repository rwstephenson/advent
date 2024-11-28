class Interval:

    def __init__(self, x, y):
        assert(isinstance(x,int))
        assert(isinstance(y,int))
        self.low = min(x,y)
        self.high = max(x,y)

    @classmethod
    def fromStr(cls,interval):
        tup = interval.split('-')
        assert(len(tup) == 2)
        return cls(int(tup[0]),int(tup[1]))

    def __str__(self):
        return "Interval({0}-{1})".format(self.low, self.high)

    def __hash__(self):
        return hash((self.low, self.high))

    def size(self,inclusive=True):
        if inclusive:
            return self.high - self.low + 1
        else:
            return self.high - self.low - 1

    def getIntersection(self, other):
        if self.low > other.high or other.low > self.high:
            return None
        elif self.low >= other.low:
            return Interval(self.low, min(self.high,other.high))
        elif self.low < other.low:
            return Interval(other.low, min(self.high,other.high))
