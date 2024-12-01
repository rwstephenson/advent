class Node:

    def __init__(self, value):
        self.value = value
        self.children = []
        self.left = None
        self.right = None

    def setChildren(self, children):
        self.children = children
        if len(self.children) == 2:
            self.left = children[0]
            self.right = children[1]

    def childrenToStr(self):
        s = self.children[0].value
        for c in self.children[1:]:
            s += ',' + c.value
        return s

    def __str__(self):
        return self.value

    def print(self):
        print("Node({}), Children[{}]".format(self.value,self.childrenToStr()))

    def __hash__(self):
        return hash(self.value)

