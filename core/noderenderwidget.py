from PySide import QtGui, QtCore

class NodeRenderWidget(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1
    
    def __init__(self, graphwidget, node):
        QtGui.QGraphicsItem.__init__(self)
        self.node = node
        self.graphwidget = graphwidget

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)
        
        self.base_width = 80
        self.base_height = 40
    
    def boundingRect(self):
        return QtCore.QRectF(0, 0,  self.base_width, self.base_height)
                             
    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(0, 0, self.base_width, self.base_height)   
        return path
    
    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        
        gradient = QtGui.QLinearGradient(0, 0, 0, self.base_height)
        gradient.setColorAt(1, QtCore.Qt.yellow)
        gradient.setColorAt(0, QtCore.Qt.darkYellow)
        
        painter.setBrush(QtGui.QBrush(gradient))
        rectangle = QtCore.QRectF(0, 0, self.base_width, self.base_height)
        painter.drawRoundRect(rectangle, 15)
        
        painter.setPen(QtGui.QColor(0,0,0))
        painter.setFont(QtGui.QFont('Sans Serif', 6))
        painter.drawText(rectangle, QtCore.Qt.AlignCenter, self.node.name)
        
    def itemChange(self, change, value):
        for x in self.node.properties.values():
            for y in x.connection_render_widgets + x.dependent_connection_render_widgets:
                y.prepareGeometryChange()
        return QtGui.QGraphicsItem.itemChange(self, change, value)
        
    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)