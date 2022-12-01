# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QEvent, pyqtSignal, Qt


# 继承自QPushButton 添加鼠标 悬浮 离开 信号
class Button(QPushButton):
    # 鼠标移入信号
    mouseEnter = pyqtSignal()
    # 鼠标移除信号
    mouseLeave = pyqtSignal()

    def __init__(self, *args):
        super(Button, self).__init__(*args)
        # 事件监听
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        # 当鼠标移入时 发射信号
        if event.type() == QEvent.Enter:
            self.mouseEnter.emit()
        if event.type() == QEvent.Leave:
            self.mouseLeave.emit()
        return super().eventFilter(obj, event)
