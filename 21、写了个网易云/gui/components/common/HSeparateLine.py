# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import QFrame


class HSeparateLine(QFrame):
    def __init__(self):
        super(HSeparateLine, self).__init__()

        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
