# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import *

from gui.pages.content.MenuType import MenuType
from gui.pages.content.child.CollectWidget import CollectWidget
from gui.pages.content.child.DownloadWidget import DownloadWidget
from gui.pages.content.child.FindMusicWidget import FindMusicWidget
from gui.pages.content.child.HomeWidget import HomeWidget
from gui.pages.content.child.KeyWordSearchWidget import KeyWordSearchWidget
from gui.pages.content.child.MyDeviceWidget import MyDeviceWidget
from gui.pages.content.child.RecentWidget import RecentWidget
from gui.pages.content.child.VideoWidget import VideoWidget


class PageStackedWidget(QStackedWidget):
    WINDOW_MIN_WIDTH = 1030

    # 所有页面
    components = []

    def __init__(self):
        super(PageStackedWidget, self).__init__()

        self.setMinimumWidth(self.WINDOW_MIN_WIDTH)

        self.initStyle()
        self.initUI()

    def initStyle(self):
        style = """

        """
        self.setStyleSheet(style)

    def initUI(self):
        findMusicWidget = FindMusicWidget(MenuType.FIND_MUSIC.value)
        self.addWidget(findMusicWidget)

        self.videoWidget = VideoWidget(MenuType.VIDEO.value)
        self.addWidget(self.videoWidget)

        myDeviceWidget = MyDeviceWidget(MenuType.MY_DEVICE.value)
        self.addWidget(myDeviceWidget)

        homeWidget = HomeWidget(MenuType.HOME.value)
        self.addWidget(homeWidget)

        self.downloadWidget = DownloadWidget(MenuType.DOWNLOAD.value)
        self.addWidget(self.downloadWidget)

        self.recentWidget = RecentWidget(MenuType.RECENT.value)
        self.addWidget(self.recentWidget)

        self.collectWidget = CollectWidget(MenuType.COLLECT.value)
        self.addWidget(self.collectWidget)

        self.keywordSearchWidget = KeyWordSearchWidget(MenuType.SEARCH.value)
        self.addWidget(self.keywordSearchWidget)

        # 初始化components
        for i in range(self.layout().count()):
            self.components.append(self.layout().itemAt(i).widget())

    # 根据tag查找组件
    def indexAt(self, tag):
        for component in self.components:
            if component.getTag() == tag:
                return component

    def setCurrentPage(self, tag):
        if tag == MenuType.RECENT.value:
            self.recentWidget.display()
        if tag == MenuType.COLLECT.value:
            self.collectWidget.display()
        if tag == MenuType.DOWNLOAD.value:
            self.downloadWidget.display()
        if tag == MenuType.VIDEO.value:
            self.videoWidget.display()
        self.setCurrentWidget(self.indexAt(tag))
