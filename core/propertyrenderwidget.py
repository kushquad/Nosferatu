from PySide import QtGui, QtCore

class PropertyRenderWidget(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 2
    
    def __init__(self, graphwidget, property):
        QtGui.QGraphicsItem.__init__(self)
        self.property = property
        self.graphwidget = graphwidget
        
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)
        
        self.base_radius = 20
        self.base_height = self.base_radius
        self.base_width = self.base_radius
    
    def boundingRect(self):
        return QtCore.QRectF(-self.base_width/2, -self.base_height/2, 2*self.base_width, 2*self.base_height)
                             
    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, self.base_width, self.base_height)
        return path
    
    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        
        gradient = QtGui.QLinearGradient(0, 0, 0, self.base_height)
        gradient.setColorAt(1, QtCore.Qt.darkRed)
        gradient.setColorAt(0, QtCore.Qt.red)
        painter.setBrush(QtGui.QBrush(gradient))
        ellipse_rectangle = QtCore.QRectF(0, 0, self.base_width, self.base_height)
        ellipse_rectangle = QtCore.QRectF(0, 0, self.base_width, self.base_height)
        painter.drawEllipse(ellipse_rectangle)
        
        painter.setPen(QtGui.QColor(0,0,0))
        painter.setFont(QtGui.QFont('Arial', 2))
        ellipse_text_rectangle = QtCore.QRectF(-self.base_width/2, -self.base_height/2, self.base_width*2, self.base_height*2)
        painter.drawText(ellipse_text_rectangle, QtCore.Qt.AlignCenter, self.property.name)
        
    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)