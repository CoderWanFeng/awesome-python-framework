# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):
    clicked = pyqtSignal(float)

    def __init__(self, *args):
        super(ProgressBar, self).__init__(*args)
        self.setTextVisible(False)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, event):
        self.clicked.emit(event.pos().x() / self.width())
