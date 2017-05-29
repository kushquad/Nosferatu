class Graph:
    def __init__(self):
        self.nodes = {}
        self.adjlist = {}
        
        # For statistics
        self.nodecount = 0
        self.edgecount = 0
    
    # The graph can access the node by reference using its id
    # The adjacency list is initialized for the node
    def add_node(self, node):
        self.nodes[node.id] = node
        self.adjlist[node.id] = set()
        self.nodecount += 1
        node.graph = self
    
    # This constructs a directed edge between nodeA and nodeB
    # This does not check for construction of cycles yet
    def add_edge(self, nodeA, nodeB):
        self.adjlist[nodeA.id].add(nodeB.id)
        self.edgecount += 1
    
    # We use topological sort to generate a schedule for single-threaded node
    # traversal. This is used internally by the execute() method.
    def schedule(self):
        def toposort(nodeid, visited, stack):
            visited[nodeid] = True
            for neighborid in self.adjlist[nodeid]:
                if not visited[neighborid]:
                    toposort(neighborid, visited, stack)
            stack.append(nodeid)
            
        visited = {id:False for id in self.nodes.keys()}
        stack = []
        for nodeid in self.nodes.keys():
            if not visited[nodeid]:
                toposort(nodeid, visited, stack)
        
        stack.reverse()
        return stack

    # Generate schedule and execute nodes in that order
    # However, this will be a bit more complex when nodes have different 
    #    execution conditions
    # This also needs to account for parellel and distributed scheduling
    def execute(self):
        schedulelist = self.schedule()
        for nodeid in schedulelist:
            self.nodes[nodeid].execute()