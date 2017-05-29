import sys
from PySide import QtCore, QtGui
    
def main():
    
    # Setup main application interface
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QWidget()
    window.setWindowTitle('Nosferatu')
    horizontal_window_layout = QtGui.QHBoxLayout(window)
    nodeprop_frame = QtGui.QFrame()
    vertical_nodeprop_frame_layout = QtGui.QVBoxLayout(nodeprop_frame)
    
    import graph as Graph
    import node
    import property
    import graphwidget
    
    graph = Graph.Graph()

    # Define a file read node
    FileReadNode = node.Node("FileRead")
    FileReadNode.add_property(property.Property('File Path'))
    FileReadNode.add_property(property.Property('File Data', proptype=property.Property.OUTPUT))
    def frexec():
        FileReadNode.properties['File Data'].set(open(FileReadNode.properties['File Path'].value).read())
    FileReadNode.execute_kernel = frexec

    # Define a line splitter node
    LineSplitterNode = node.Node("LineSplitter")
    LineSplitterNode.add_property(property.Property('Text'))
    LineSplitterNode.add_property(property.Property('Lines', proptype=property.Property.OUTPUT))
    def lsexec():
        LineSplitterNode.properties['Lines'].set(LineSplitterNode.properties['Text'].value.split('\n'))
    LineSplitterNode.execute_kernel = lsexec

    # Define a list length node
    ListLengthNode = node.Node("ListLength")
    ListLengthNode.add_property(property.Property('List'))
    ListLengthNode.add_property(property.Property('Length', proptype=property.Property.OUTPUT))
    def llexec():
        ListLengthNode.properties['Length'].set(len(ListLengthNode.properties['List'].value))
    ListLengthNode.execute_kernel = llexec
    
    # Define a list length node
    PrintNode = node.Node("Print")
    PrintNode.add_property(property.Property('Text'))
    def pexec():
        print str(PrintNode.properties['Text'].value)
    PrintNode.execute_kernel = pexec
    
    # Add nodes to graph (UI action)
    graph.add_node(FileReadNode)
    graph.add_node(LineSplitterNode)
    graph.add_node(ListLengthNode)
    graph.add_node(PrintNode)

    # Connect properties of nodes (UI action)
    FileReadNode.properties['File Path'].set('C:\Users\Kush\Desktop\Nosferatu\core\graph.py')
    FileReadNode.properties['File Data'].connect(LineSplitterNode.properties['Text'])
    LineSplitterNode.properties['Lines'].connect(ListLengthNode.properties['List'])
    
    graphwidget = graphwidget.GraphWidget()
    horizontal_window_layout.addWidget(graphwidget)
    
    for node in graph.nodes.values():
        vertical_nodeprop_frame_layout.addWidget(node.initialize_ui())
        node.draw_node(graphwidget)
    
    for node in graph.nodes.values():
        for property in node.properties.values():
            for connected_property in property.connected_properties:
                property.draw_property_connection(graphwidget, connected_property)
            
    horizontal_window_layout.addWidget(nodeprop_frame)
    
    execute_button = QtGui.QPushButton('Execute')
    execute_button.clicked.connect(graph.execute)
    vertical_nodeprop_frame_layout.addWidget(execute_button)
    
    window.show()
    sys.exit(app.exec_())
    
main()