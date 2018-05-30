import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsWidget, QGraphicsGridLayout, QGraphicsRectItem
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QRectF




class PathTrace():
    def __init__(self, width, height, nx, ny):
        Settings.WIDTH = width
        Settings.HEIGHT = height
        Settings.NUM_BLOCKS_X = nx
        Settings.NUM_BLOCKS_Y = ny
        self.initUI()
    
    def initUI(self):
        app = QApplication(sys.argv)
        a = QS()
        b = QV()
        b.setScene(a)
        b.show()
        sys.exit(app.exec_())



class Settings():
        WIDTH = 0
        HEIGHT = 0
        NUM_BLOCKS_X = 0
        NUM_BLOCKS_Y = 0



class RectangleWidget(QGraphicsWidget):
    def __init__(self, rect, path=False, item=False, parent=None):
        super(RectangleWidget, self).__init__(parent)
        self.rect = rect
        self.path = path
        self.item = item

    def paint(self, painter, *args, **kwargs):
        painter.drawRect(self.rect)
        if self.path:
            brush = QBrush(Qt.red)
            painter.fillRect(self.rect, brush)
        
        if self.item:
            brush = QBrush(Qt.blue)
            painter.fillRect(self.rect, brush)




class QS(QtWidgets.QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        width = Settings.NUM_BLOCKS_X *(Settings.WIDTH+1)
        height = Settings.NUM_BLOCKS_Y * (Settings.HEIGHT+1)
        self.setSceneRect(0, 0, height, width)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        
        layout = QGraphicsGridLayout()
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)
        
        form = QGraphicsWidget()
        form.setLayout(layout)
        
        for i in range(Settings.NUM_BLOCKS_X):
            layout.setRowSpacing(i, 0)
            layout.setRowMaximumHeight(i, Settings.HEIGHT)
            for j in range(Settings.NUM_BLOCKS_Y):
                layout.setColumnSpacing(j, 0)
                layout.setColumnMaximumWidth(j, Settings.WIDTH)
                if j-i == 1:
                    rect = RectangleWidget(QRectF(0,0,Settings.WIDTH,Settings.HEIGHT), path=True)
                elif j-i == 3:
                    rect = RectangleWidget(QRectF(0,0,Settings.WIDTH,Settings.HEIGHT), item=True)
                else:
                    rect = RectangleWidget(QRectF(0,0,Settings.WIDTH,Settings.HEIGHT))

                layout.addItem(rect, i, j)

        self.addItem(form)
        



class QV(QtWidgets.QGraphicsView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    PathTrace(25, 25, 18, 36)

