class Node(object):
    # Assign a unique ID to each node using a class counter
    _instancecount = 1
    
    def __init__(self, name=None, graph=None):
        # Incrementing instancecount assigns a new ID to the next created node
        self.id = Node._instancecount
        Node._instancecount += 1
        
        self.name = name
        self.graph = graph
        self.properties = {}
        self.execute_kernel = None
        self.UIwidget = None
        
        self.x = 0
        self.y = 80*Node._instancecount
        
    def add_property(self, property):
        property.node = self
        self.properties[property.name] = property
    
    def connect(self, node):
        self.graph.add_edge(self, node)

    def execute(self):
        print "Executing : {0}:{1}".format(self.id, self.name)
        self.execute_kernel()
        if self.UIwidget:
            self.refresh()
    
    def initialize_ui(self):
        from PySide import QtCore, QtGui
        
        node_ui_widget = QtGui.QFrame()
        node_ui_widget.setLineWidth(2)
        node_ui_widget.setFrameShape(QtGui.QFrame.StyledPanel)
        node_ui_layout = QtGui.QVBoxLayout(node_ui_widget)
        
        # Label displays the name of the node
        label = QtGui.QLabel(self.name)
        node_ui_layout.addWidget(label)
        
        # Render each property separately, add to node UI layout
        for property in self.properties.values():
            propertylayout = property.initialize_ui()
            node_ui_layout.addLayout(propertylayout)
            
        # Add ui components to widget in case its needed later
        # Property layouts can be accessed using the self.properties object itself
        self.UIwidget = node_ui_widget
        self.UIwidget.label = label
        
        return node_ui_widget
    
    def draw_node(self, graphwidget):
        import noderenderwidget
        
        node_render_widget = noderenderwidget.NodeRenderWidget(graphwidget, self)
        node_render_widget.setPos(self.x, self.y)
        graphwidget.scene().addItem(node_render_widget)
        
        # Draw property connectors exposed for this node in the graph UI
        for property in self.properties.values():
            property.draw_property(graphwidget, self)
            if property.property_role==property.OUTPUT:
                property.property_render_widget.setPos(30, 30)
            else:
                property.property_render_widget.setPos(30, -10)
            property.property_render_widget.setParentItem(node_render_widget)
    
    def refresh(self):
        self.UIwidget.label.setText(self.name)
        for property in self.properties.values():
            property.refresh()