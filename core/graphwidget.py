from PySide import QtCore, QtGui
import math

class GraphWidget(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        
        self.widget_scene = QtGui.QGraphicsScene(self)
        self.widget_scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.widget_scene.setSceneRect(-320, -240, 640, 480)
        self.setScene(self.widget_scene)
        
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setBackgroundBrush(QtGui.QColor.fromHsv(225,7,45))
        self.scaleView(0.8)
        
    # Trigger view resize on a mouse wheel scroll
    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, event.delta()/240.0))
        
    # Does the actual scaling of the view ensuring scale factor
    # is within limits
    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)