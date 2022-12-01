# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import qtawesome as qta


class MenuButton(QPushButton):
    click = pyqtSignal(int)

    def __init__(self, index, text, icon=None):
        super(MenuButton, self).__init__()

        self.index = index
        self.setText(text)
        if icon:
            self.setIcon(qta.icon('fa.' + icon, color='#373737'))

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.initStyle()

        self.clicked.connect(lambda: self.click.emit(self.index))

    def initStyle(self):
        style = """
        MenuButton{
            color:#454545;
            border:none;
            text-align:left;
            height:45px;
            font-size:20px;
            padding-left:5px;
        }
        MenuButton:hover{
            background:#F6F6F7;
        }
        """
        self.setStyleSheet(style)

    def setSelected(self, selected):
        if selected:
            self.setStyleSheet(
                "MenuButton{border:none;text-align:left;height:45px;font-size:20px;padding-left:5px;color:#313131;font-weight:bold;background:#F6F6F7;}")
        else:
            self.initStyle()

    def getIndex(self):
        return self.index


class Win(QWidget):
    def __init__(self):
        super(Win, self).__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        button = MenuButton("发现歌曲")
        button.setSelected(True)
        layout.addWidget(button)

