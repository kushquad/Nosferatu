from PySide import QtCore, QtGui

class NodeDesigner(QtGui.QFrame):
    def __init__(self):
        QtGui.QFrame.__init__(self)
        
        self.mainlayout = QtGui.QHBoxLayout(self)
        self.setWindowTitle('Node Designer')
        
        self.node_template = \
        '''
        from core.node import Node
        
        def kernel_function():
            {execute_kernel}
            
        class {nodename}Node(Node):
            _nodecount = 1
            
            def __init__(self):
                Node.__init__(self)
                self.nodeid = _nodecount
                _nodecount += 1
                self.name = "{nodename}Node{id}".format(id=self.nodeid)
                self.description = {description}
                
                self.execute_kernel = kernel_function
        '''
        
        self.basic_node_layout = QtGui.QVBoxLayout()
        self.node_property_layout = QtGui.QVBoxLayout()
        self.mainlayout.addLayout(self.basic_node_layout)
        self.mainlayout.addLayout(self.node_property_layout)
        
        self.node_name_horizontal_layout = QtGui.QHBoxLayout()
        self.label_node_name = QtGui.QLabel('Name')
        self.label_node_name.setFixedWidth(100)
        self.lineEdit_node_name = QtGui.QLineEdit()
        self.node_name_horizontal_layout.addWidget(self.label_node_name)
        self.node_name_horizontal_layout.addWidget(self.lineEdit_node_name)
        self.basic_node_layout.addLayout(self.node_name_horizontal_layout)
        
        self.node_description_horizontal_layout = QtGui.QHBoxLayout()
        self.label_node_description = QtGui.QLabel('Description')
        self.label_node_description.setFixedWidth(100)
        self.lineEdit_node_description = QtGui.QLineEdit()
        self.node_description_horizontal_layout.addWidget(self.label_node_description)
        self.node_description_horizontal_layout.addWidget(self.lineEdit_node_description)
        self.basic_node_layout.addLayout(self.node_description_horizontal_layout)
        
        self.kernel_function_horizontal_layout = QtGui.QHBoxLayout()
        self.label_kernel_function = QtGui.QLabel('Kernel Function')
        self.label_kernel_function.setFixedWidth(100)
        self.textEdit_kernel_function = QtGui.QTextEdit()
        self.kernel_function_horizontal_layout.addWidget(self.label_kernel_function)
        self.kernel_function_horizontal_layout.addWidget(self.textEdit_kernel_function)
        self.basic_node_layout.addLayout(self.kernel_function_horizontal_layout)
        
        self.label_property_editor = QtGui.QLabel('Property Editor')
        self.node_property_layout.addWidget(self.label_property_editor)
        self.tableWidget_property_editor = QtGui.QTableWidget()
        self.node_property_layout.addWidget(self.tableWidget_property_editor)
