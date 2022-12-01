# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import *
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import *


class LyricWidget(QWidget):
    # 窗体的最小宽高
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 120

    def __init__(self):
        super(LyricWidget, self).__init__()
        self.setMinimumSize(self.WINDOW_MIN_WIDTH, self.WINDOW_MIN_HEIGHT)
        self.setCursor(QCursor(Qt.ClosedHandCursor))

        self.setWindowFlags(Qt.FramelessWindowHint)

        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.installEventFilter(self)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.raise_()

        self.display = QLabel()
        self.display.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.display.setStyleSheet("font-size:35px;color:#EC4141;")
        layout.addWidget(self.display)

    def setLyric(self, lyric):
        self.display.setText(lyric)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag = True
            self.dragPosition = event.pos()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.drag:
            self.move(event.globalPos() - self.dragPosition)

    def mouseReleaseEvent(self, event):
        self.drag = False

    def eventFilter(self, obj, event):
        # 当鼠标移入时 发射信号
        if event.type() == QEvent.Enter:
            self.setWindowOpacity(0.9)
            pass
        if event.type() == QEvent.Leave:
            pass
            self.setWindowOpacity(0.4)
        return super().eventFilter(obj, event)
