# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.utils.ImgConverter import ToCircleImg


class LogoWidget(QWidget):
    mouseDoubleClick = pyqtSignal()

    def __init__(self):
        super(LogoWidget, self).__init__()

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.initUI()

    def initUI(self):
        logoUrl = '../../resource/img/netease.png'
        logoSize = 32

        layout = QHBoxLayout()
        self.setLayout(layout)

        logo = QLabel()
        logo.setPixmap(ToCircleImg(logoUrl, logoSize, logoSize, self))
        layout.addWidget(logo)

        title = QLabel("网易云音乐")
        title.setStyleSheet("font-size:23px;color:#FFFFFF;font-weight:bold;")
        layout.addWidget(title)

        layout.addStretch(1)

    # 重写鼠标双击事件
    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClick.emit()
