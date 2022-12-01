# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dao.Redis import redis
from gui.pages.navbar.LogoWidget import LogoWidget
from gui.pages.navbar.MenuWidget import MenuWidget
from gui.pages.navbar.SearchWidget import SearchWidget


class NavBar(QWidget):
    moveSignal = pyqtSignal(QPoint)
    minimizeSignal = pyqtSignal()
    maximizeSignal = pyqtSignal()
    restoreSignal = pyqtSignal()
    closeSignal = pyqtSignal()

    microphoneSignal = pyqtSignal()
    avatarSignal = pyqtSignal()
    settingSignal = pyqtSignal()
    miniModelSignal = pyqtSignal()

    def __init__(self):
        super(NavBar, self).__init__()

        self.setCursor(QCursor(Qt.ArrowCursor))

        self.initStyle()
        self.initParams()
        self.initUI()

    def initStyle(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        style = """
        NavBar{
           background-color: #EC4141;
        }
        QPushButton{
            border:none;
        }
        """
        self.setStyleSheet(style)

    def initParams(self):
        self.isMaximize = redis.getValue('isMaximize', 0)

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        logoWidget = LogoWidget()
        logoWidget.setFixedWidth(185)
        logoWidget.mouseDoubleClick.connect(self.launchMaximizeOrRestoreSignal)
        layout.addWidget(logoWidget)

        space = QLabel()
        space.setFixedWidth(95)
        layout.addWidget(space)

        searchWidget = SearchWidget()

        searchWidget.microphoneSignal.connect(self.microphoneSignal)
        layout.addWidget(searchWidget)

        layout.addStretch(1)

        self.menuWidget = MenuWidget()
        self.menuWidget.avatarSignal.connect(self.avatarSignal)
        self.menuWidget.settingSignal.connect(self.settingSignal)
        self.menuWidget.miniModelSignal.connect(self.miniModelSignal)
        self.menuWidget.minimizeSignal.connect(self.minimizeSignal)
        self.menuWidget.maximizeSignal.connect(self.launchMaximizeOrRestoreSignal)
        self.menuWidget.closeSignal.connect(self.closeSignal)
        self.initMaximizeIconName()
        layout.addWidget(self.menuWidget)

    def initMaximizeIconName(self):
        if self.isMaximize:
            self.menuWidget.setMaximizeIconName('window-restore')
        else:
            self.menuWidget.setMaximizeIconName('window-maximize')

    def launchMaximizeOrRestoreSignal(self):
        if (self.isMaximize):
            self.restoreSignal.emit()
            self.menuWidget.setMaximizeIconName('window-maximize')
            self.isMaximize = 0
        else:
            self.maximizeSignal.emit()
            self.menuWidget.setMaximizeIconName('window-restore')
            self.isMaximize = 1

    def mousePressEvent(self, event):
        # if event.button() == Qt.LeftButton and event.pos().x() < self.menuWidget.pos().x():
        if event.button() == Qt.LeftButton:
            self.drag = True
            self.dragPosition = event.pos()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.drag:
            if self.isMaximize:
                self.isMaximize = 0
                self.restoreSignal.emit()
                self.menuWidget.setMaximizeIconName('window-maximize')
            self.moveSignal.emit(event.globalPos() - self.dragPosition)

    def mouseReleaseEvent(self, event):
        self.drag = False
