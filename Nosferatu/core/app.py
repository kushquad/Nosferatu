import sys
from PySide import QtCore, QtGui
    
def main():
    
    # Setup main application interface
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QWidget()
    vertical_window_layout = QtGui.QHBoxLayout(window)
    nodeprop_frame = QtGui.QFrame()
    vertical_window_layout.addWidget(nodeprop_frame)
    vertical_nodeprop_frame_layout = QtGui.QVBoxLayout(nodeprop_frame)
    
    import graph as Graph
    import node
    import property
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

    # Add nodes to graph (UI action)
    graph.add_node(FileReadNode)
    graph.add_node(LineSplitterNode)
    graph.add_node(ListLengthNode)

    # Connect properties of nodes (UI action)
    FileReadNode.properties['File Path'].set('C:\Users\Kush\Desktop\Nosferatu\core\graph.py')
    FileReadNode.properties['File Data'].connect(LineSplitterNode.properties['Text'])
    LineSplitterNode.properties['Lines'].connect(ListLengthNode.properties['List'])
    
    execute_button = QtGui.QPushButton('Execute')
    execute_button.clicked.connect(graph.execute)
    vertical_window_layout.addWidget(execute_button)
    
    for node in graph.nodes.values():
        vertical_nodeprop_frame_layout.addWidget(node.initialize_ui())
    window.show()
    
    sys.exit(app.exec_())
    
main()