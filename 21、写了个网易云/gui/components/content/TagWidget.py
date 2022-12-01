# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import QWidget


class TagWidget(QWidget):

    def __init__(self, tag):
        super(TagWidget, self).__init__()
        self.tag = tag

    def getTag(self):
        return self.tag
