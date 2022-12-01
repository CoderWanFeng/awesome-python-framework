# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSlider

from dao.Redis import redis
from gui.components.common.CommonButton import CommonButton


class ControlWidget(QWidget):
    volumnSignal = pyqtSignal(int)

    def __init__(self):
        super(ControlWidget, self).__init__()

        self.initParams()
        self.initStyle()
        self.initUI()

    def initStyle(self):
        style = """
               QPushButton{
                   border:none;
               }
               """
        self.setStyleSheet(style)

    def initParams(self):
        self.originalVolumn = redis.getValue('volumn', 50)
        self.trumpetStatus = redis.getValue('trumpet', True)

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        self.setLayout(layout)

        self.tone = CommonButton(iconName='superpowers')
        layout.addWidget(self.tone)

        self.trumpet = CommonButton()
        self.setTrumpetStatus()
        self.trumpet.clicked.connect(self.changeTrumpetStatus)
        layout.addWidget(self.trumpet)

        self.volumn = QSlider(Qt.Horizontal)
        self.volumn.setMaximum(100)
        self.setVolumn()
        self.volumn.valueChanged.connect(self.volumnChangedHandle)
        self.volumn.setObjectName('volumn')
        layout.addWidget(self.volumn)

        self.list = CommonButton(iconName='align-justify')
        layout.addWidget(self.list)

    def volumnChangedHandle(self, value):
        if (value == 0):
            self.trumpet.resetIconName('bell-slash-o')
        else:
            self.trumpet.resetIconName('bell-o')
        self.volumnSignal.emit(value)

    def setTrumpetStatus(self):
        if self.trumpetStatus:
            self.trumpet.resetIconName('bell-o')
        else:
            self.trumpet.resetIconName('bell-slash-o')

    def setVolumn(self):
        if self.trumpetStatus:
            self.volumn.setValue(self.originalVolumn)
        else:
            self.volumn.setValue(0)

    def changeTrumpetStatus(self):
        if self.trumpetStatus:
            self.trumpet.resetIconName('bell-slash-o')
            self.originalVolumn = self.volumn.value()
            self.volumn.setValue(0)
        else:
            self.trumpet.resetIconName('bell-o')
            self.volumn.setValue(self.originalVolumn)
        self.trumpetStatus = not self.trumpetStatus
