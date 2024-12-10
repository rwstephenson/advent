import graphviz

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.left = None
        self.right = None

    def setChildren(self, children):
        self.children = children
        self.left = children[0]
        self.right = children[1]

    def childrenToStr(self):
        s = ""
        if len(self.children) > 0:
            s = str(self.children[0].value)
            for c in self.children[1:]:
                s += ',' + str(c.value)
        return s

    def visualiseWalk(self,seen,dot,labelEdges=False):
        dot.node(self.value)
        seen.add(hash(self))
        for n in self.children:
            dot.node(n.value,n.value)
            if labelEdges:
                dot.edge(self.value,n.value,str(self.value) + "-" + str(n.value))
            else:
                dot.edge(self.value,n.value)
            if hash(n) not in seen:
                n.visualiseWalk(seen,dot)

    def visualise(self):
        dot = graphviz.Graph('myGraph')
        dot.graph_attr['layout'] = 'neato'
        self.visualiseWalk(set(),dot)
        dot.render('my-graph.gv', format='png', view=True)

    def __str__(self):
        return str(self.value)

    def print(self):
        print("Node({}), Children[{}]".format(self.value,self.childrenToStr()))

    def __hash__(self):
        return hash(self.value)

