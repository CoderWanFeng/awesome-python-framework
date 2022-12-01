# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, pyqtSignal
import qtawesome as qta
from functools import partial

# 继承自Button 实现按钮背景图片的设置 及 鼠标悬浮时的变色
from gui.components.common.Button import Button


class HoverButton(Button):
    tagSignal = pyqtSignal(object)

    # 默认值
    activeColor = '#FFFFFF'
    inActiveColor = '#F8CECE'
    cursor = Qt.PointingHandCursor

    def __init__(self, *args, **kwargs):
        super(HoverButton, self).__init__(*args)

        style = "HoverButton{border:none;}"

        # 图标颜色初始化
        activeColor = kwargs.get('activeColor')
        if activeColor != None:
            self.activeColor = activeColor
        inActiveColor = kwargs.get('inActiveColor')
        if inActiveColor != None:
            self.inActiveColor = inActiveColor

        # 按钮文字
        text = kwargs.get('text')
        if text != None:
            self.setText(text)
            style += "HoverButton{color:" + self.inActiveColor + ";}"
            style += "HoverButton:hover{color:" + self.activeColor + ";}"
        # 判断iconName是否存在
        iconName = kwargs.get('iconName')
        if iconName != None:
            self.iconName = iconName
            self.setIcon(qta.icon("fa." + self.iconName, color=self.inActiveColor))
            if self.inActiveColor != self.activeColor:
                self.mouseEnter.connect(partial(self.resetIcon, 1))
                self.mouseLeave.connect(partial(self.resetIcon, 0))

        # 光标初始化
        cursor = kwargs.get('cursor')
        if cursor != None:
            self.cursor = cursor
        self.setCursor(QCursor(self.cursor))
        self.setStyleSheet(style)

        # 按钮标记
        tag = kwargs.get('tag')
        if tag != None:
            self.clicked.connect(lambda: self.tagSignal.emit(tag))

    # status为1 则为激活状态 否则为不激活状态
    def resetIcon(self, status):
        if status == 1:
            self.setIcon(qta.icon("fa." + self.iconName, color=self.activeColor))
        else:
            self.setIcon(qta.icon("fa." + self.iconName, color=self.inActiveColor))

    def resetIconName(self, iconName):
        self.iconName = iconName
        self.resetIcon(0)

    def resetIconColor(self, inActiveColor, activeColor):
        self.activeColor = activeColor
        self.inActiveColor = inActiveColor
        self.resetIcon(0)
