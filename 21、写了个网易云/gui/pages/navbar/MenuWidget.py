# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.content.HoverButton import HoverButton
from gui.utils.ImgConverter import ToCircleImg


class MenuWidget(QWidget):
    avatarUrl = '../../resource/img/avatar.png'
    avatarSize = 32

    avatarSignal = pyqtSignal()
    settingSignal = pyqtSignal()
    miniModelSignal = pyqtSignal()
    minimizeSignal = pyqtSignal()
    maximizeSignal = pyqtSignal()
    closeSignal = pyqtSignal()

    def __init__(self):
        super(MenuWidget, self).__init__()

        self.initStyle()
        self.initUI()

    def initStyle(self):
        style = """
        #avatar{
            width:32px;
            height:32px;
        }
        #profile{
            color:#FBD9D9;  
        }
        #profile:hover{
            color:#ffffff;   
        }
        #minimize{
            padding-bottom:9px;
        }
        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QHBoxLayout()
        layout.setSpacing(24)
        self.setLayout(layout)

        avatar = QPushButton()
        avatar.setIcon(QIcon(ToCircleImg(self.avatarUrl, self.avatarSize, self.avatarSize, self)))
        avatar.setIconSize(QSize(self.avatarSize, self.avatarSize))
        avatar.setCursor(QCursor(Qt.PointingHandCursor))
        avatar.setObjectName("avatar")
        layout.addWidget(avatar)

        profile = HoverButton('乐乐', iconName='caret-down')
        profile.setObjectName('profile')
        layout.addWidget(profile)

        theme = HoverButton(iconName='diamond')
        layout.addWidget(theme)

        setting = HoverButton(iconName='cog')
        setting.setObjectName('setting')
        layout.addWidget(setting)

        miniModel = HoverButton(iconName='desktop')
        self.setObjectName('miniModel')
        layout.addWidget(miniModel)

        self.minimize = HoverButton(iconName='window-minimize')
        self.minimize.setObjectName("minimize")
        layout.addWidget(self.minimize)

        self.maximize = HoverButton(iconName='window-maximize')
        self.maximize.setObjectName('maximize')
        layout.addWidget(self.maximize)

        self.close = HoverButton(iconName='window-close')
        self.close.setObjectName('close')
        layout.addWidget(self.close)

        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def on_avatar_clicked(self):
        self.avatarSignal.emit()

    @pyqtSlot()
    def on_setting_clicked(self):
        self.settingSignal.emit()

    @pyqtSlot()
    def on_miniModel_clicked(self):
        self.miniModelSignal.emit()

    @pyqtSlot()
    def on_minimize_clicked(self):
        self.minimizeSignal.emit()

    @pyqtSlot()
    def on_maximize_clicked(self):
        self.maximizeSignal.emit()

    @pyqtSlot()
    def on_close_clicked(self):
        self.closeSignal.emit()

    def setMaximizeIconName(self, iconName):
        self.maximize.resetIconName(iconName)

