class Property(object):
    INPUT = 0
    OUTPUT = 1
    
    LATCHED = 0
    TRIGGERED = 2
    
    LABEL_WIDTH = 120
    
    def __init__(self, name, desc=None, proptype=INPUT|LATCHED,
                 promoted=False, required=False):
        
        self.name = name
        self.desc = desc
        self.property_role = proptype & Property.OUTPUT
        self.property_behavior = proptype & Property.TRIGGERED
        
        # Promoted refers to whether the property is exposed as a connectable 
        # attribute on a node (might be either input or output)
        self.promoted = promoted
        
        # Required refers to whether the property needs to have a value
        # for the node to execute.
        
        # All required input properties need a value before they the node can execute
        # A node finishes execution only when all required output properties have received a value
        self.required = required
        
        # Value contained by the property
        self.value = None
        
        self.connected_properties = set()
        self.dependent_properties = set()
        self.connected = False
        
        self.node = None
        self.property_layout = None
        
        self.property_render_widget = None
        self.connection_render_widgets = []
        self.dependent_connection_render_widgets = []
        
    def clear(self):
        self.value = None
    
    def set(self, value):
        self.value = value
        #self.node.dirty_flag = True
        if self.property_role == Property.OUTPUT:
            for property in self.connected_properties:
                property.set(self.value)
    
    def get(self):
        return self.value
    
    def connect(self, property):
        self.connected_properties.add(property)
        property.dependent_properties.add(self)
        self.node.connect(property.node)
        self.connected = True
        property.connected = True
        
    def disconnect(self, property):
        self.connected_properties.remove(property)
        property.dependent_properties.remove(self)
        #self.node.disconnect(property.node)
    
    def setProperty(self, value):
        self.value = value
        
    def initialize_ui(self):
        from PySide import QtCore, QtGui
        property_layout = QtGui.QHBoxLayout()
            
        # Render property name
        property_heading = QtGui.QLabel(self.name)
        property_heading.setToolTip(self.desc)
        property_heading.setFixedWidth(Property.LABEL_WIDTH)
        property_layout.addWidget(property_heading)
        
        # Render property value
        property_value = QtGui.QTextEdit(unicode(self.value))
        property_value.setToolTip(self.desc)
        property_value.textChanged.connect(lambda : self.setProperty(property_value.toPlainText()))
        property_layout.addWidget(property_value)
        
        if self.property_role==Property.OUTPUT or self.connected:
            property_value.setReadOnly(True)
        
        # Make UI components accessible later by storing a reference 
        self.property_layout = property_layout
        self.property_layout.heading = property_heading
        self.property_layout.value = property_value
        
        return property_layout
    
    def draw_property(self, graphwidget, noderenderwidget):
        import propertyrenderwidget
        
        property_render_widget = propertyrenderwidget.PropertyRenderWidget(graphwidget, self)
        graphwidget.scene().addItem(property_render_widget)
        self.property_render_widget = property_render_widget
    
    def draw_property_connection(self, graphwidget, otherproperty):
        import connectionrenderwidget
        
        connection_render_widget = connectionrenderwidget.ConnectionRenderWidget(graphwidget,
                                   self.property_render_widget, otherproperty.property_render_widget)
        graphwidget.scene().addItem(connection_render_widget)
        self.connection_render_widgets.append(connection_render_widget)
        otherproperty.dependent_connection_render_widgets.append(connection_render_widget)
        
    def refresh(self):
        self.property_layout.heading.setText(self.name)
        self.property_layout.value.setText(unicode(self.value))