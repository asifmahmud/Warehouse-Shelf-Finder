import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt

class PathTrace(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300,100,900,600)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawBrushes(qp)
        qp.end()

    def drawBrushes(self, qp):
        brush = QBrush(Qt.HorPattern)
        qp.setBrush(brush)
        qp.drawRect(0,0, 900, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = PathTrace()
    sys.exit(app.exec_())

