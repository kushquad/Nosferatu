from PySide import QtGui, QtCore

class ConnectionRenderWidget(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 3
     
    def __init__(self, graphwidget, property_render_widget, other_property_render_widget):
        QtGui.QGraphicsItem.__init__(self)
        
        self.driver_property_widget = property_render_widget
        self.driven_property_widget = other_property_render_widget
        self.graphwidget = graphwidget
        
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)
        
        self.arrow_size = 2
    
    def boundingRect(self):
        self.sourcePoint = self.driver_property_widget.scenePos()
        self.destPoint = self.driven_property_widget.scenePos()
        
        if not self.sourcePoint or not self.destPoint:
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + self.arrow_size) / 2.0

        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)
        
    # If property is rendered using a circle, finds the actual points
    # to connect on the edge of the circles to connect with a line
    def clip_points(p1, p2, r1, r2):
        import math
        
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        
        d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if d==0:
            return (p1,p2)
        
        b = ((x2-x1)/d, (y2-y1)/d)
        
        nx1 = x1 + r1*b[0]
        ny1 = y1 + r1*b[1]
        nx2 = x1 + (d-r1)*b[0]
        ny2 = y2 + (d-r1)*b[1]
        
        return (QtCore.QPointF(nx1, ny1), QtCore.QPointF(nx2, ny2))
    
    def paint(self, painter, option, widget):
        import math
        
        start_point = self.driver_property_widget.scenePos()
        end_point = self.driven_property_widget.scenePos()
        start_point_radius = self.driver_property_widget.base_radius
        end_point_radius = self.driven_property_widget.base_radius
        
        #new_start_point, new_end_point = self._clip_points(start_point, end_point, start_point_radius, end_point_radius)
        
        line = QtCore.QLineF(start_point, end_point)
        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)

        angle = math.acos(line.dx()/line.length())
        if line.dy() >= 0:
            angle = 2*math.pi - angle

        destArrowP1 = end_point + QtCore.QPointF(math.sin(angle - math.pi / 3) * self.arrow_size,
                                                     math.cos(angle - math.pi / 3) * self.arrow_size)
        destArrowP2 = end_point + QtCore.QPointF(math.sin(angle - math.pi + math.pi / 3) * self.arrow_size,
                                                     math.cos(angle - math.pi + math.pi / 3) * self.arrow_size)

        painter.setBrush(QtCore.Qt.white)
        painter.drawPolygon(QtGui.QPolygonF([line.p2(), destArrowP1, destArrowP2]))
        
    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)