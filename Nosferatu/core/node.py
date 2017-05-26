class Node(object):
    # Assign a unique ID to each node using a class counter
    _instancecount = 1
    
    def __init__(self, name, graph=None):
        # Incrementing instancecount assigns a new ID to the next created node
        self.id = Node._instancecount
        Node._instancecount += 1
        
        self.name = name
        self.graph = graph
        self.properties = {}
        self.execute_kernel = None
        self.UIwidget = None
        
    def add_property(self, property):
        property.node = self
        self.properties[property.name] = property
    
    def connect(self, node):
        self.graph.add_edge(self, node)

    def execute(self):
        self.execute_kernel()
        if self.UIwidget:
            self.refresh()
        print "Executing : {0}:{1}".format(self.id, self.name)
    
    def initialize_ui(self):
        from PySide import QtCore, QtGui
        
        nodewidget = QtGui.QWidget()
        nodelayout = QtGui.QVBoxLayout(nodewidget)
        
        # Label displays the name of the node
        label = QtGui.QLabel(self.name)
        nodelayout.addWidget(label)
        
        # Render each property separately, add to node UI layout
        for property in self.properties.values():
            propertylayout = property.initialize_ui()
            nodelayout.addLayout(propertylayout)
            
        # Add ui components to widget in case its needed later
        # Property layouts can be accessed using the self.properties object itself
        self.UIwidget = nodewidget
        self.UIwidget.label = label
        
        return nodewidget
        
    def refresh(self):
        self.UIwidget.label.setText(self.name)
        for property in self.properties.values():
            property.refresh()
'''
Test Suite
a = Node("Read")
b = Node("Write")
print a.id, a.name
print b.id, b.name

class PrintNode(Node):
    def __init__(self):
        super(PrintNode, self).__init__("Print")
    def execute(self):
        print "Printing"

p = PrintNode()
print p.execute()
print p.id, p.name
'''