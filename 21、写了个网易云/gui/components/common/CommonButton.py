# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
import qtawesome as qta


class CommonButton(QPushButton):
    cursor = Qt.PointingHandCursor

    tagSignal = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(CommonButton, self).__init__(*args)

        cursor = kwargs.get('cursor')
        if cursor != None:
            self.cursor = cursor
        self.setCursor(QCursor(self.cursor))

        self.color = kwargs.get('color')

        iconName = kwargs.get('iconName')
        if iconName != None:
            self.setIcon(qta.icon('fa.' + iconName, color=self.color))

        self.tag = kwargs.get('tag')
        self.clicked.connect(self.tagSignalHandle)

    def resetIconName(self, iconName):
        self.setIcon(qta.icon('fa.' + iconName, color=self.color))

    def tagSignalHandle(self):
        if self.tag != None:
            self.tagSignal.emit(self.tag)
