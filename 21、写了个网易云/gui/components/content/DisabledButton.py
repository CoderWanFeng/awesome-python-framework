# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qtawesome as qta


class DisabledButton(QPushButton):
    inActiveColor = '#F2BABA'
    activeColor = '#ffffff'

    def __init__(self, *args, **kwargs):
        super(DisabledButton, self).__init__(*args)

        self.iconName = kwargs.get('iconName')
        self.setButtonStatus(kwargs.get('disabled', True))

    def setButtonStatus(self, disabled):
        if disabled:  # 禁用
            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setIcon(qta.icon("fa." + self.iconName, color=self.inActiveColor))
        else:
            self.setCursor(QCursor(Qt.PointingHandCursor))
            self.setIcon(qta.icon("fa." + self.iconName, color=self.activeColor))
        self.disabled = disabled

    def isDisabled(self):
        return self.disabled
