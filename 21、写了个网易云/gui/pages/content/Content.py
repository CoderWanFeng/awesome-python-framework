# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from bean.RecodeStack import recodeStack
from gui.pages.GlobalSignal import globalSignal
from gui.pages.content.MenuType import MenuType
from gui.pages.content.MenuListWidget import MenuListWidget
from gui.pages.content.PageStackedWidget import PageStackedWidget


class Content(QSplitter):
    backwardButtonFirst = True

    def __init__(self):
        super(Content, self).__init__()

        self.setChildrenCollapsible(False)
        self.setCursor(QCursor(Qt.ArrowCursor))

        self.initStyle()
        self.initUI()

    def initStyle(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        style = """
            Content{
                background:#ffffff;
            }
            QSplitter{
                width:2px;
            }
        """
        self.setStyleSheet(style)

    def initUI(self):
        # 注意加载顺序
        self.pages = PageStackedWidget()

        self.menus = MenuListWidget()
        self.menus.itemClicked.connect(self.setPageCurrentIndex)
        self.menus.setCurentIndex(MenuType.FIND_MUSIC.value)

        self.addWidget(self.menus)
        self.addWidget(self.pages)
        # 设置拉伸因子
        self.setStretchFactor(0, 0)
        self.setStretchFactor(1, 1)

        # 页面跳转
        globalSignal.pageIndexSignal.connect(self.setPageCurrentIndexI)
        globalSignal.keywordSignalI.connect(self.searchMusicBykeywordI)

    # 设置页面
    def setPageCurrentIndex(self, index):
        self.recodeStackHandle(index)
        self.pages.setCurrentPage(index)

    # 查询音乐
    def searchMusicBykeyword(self, keyword):
        self.recodeStackHandle(MenuType.SEARCH.value, keyword)
        self.menus.resetComponents()
        self.pages.setCurrentPage(MenuType.SEARCH.value)
        self.pages.keywordSearchWidget.searchMusicBykeyword(keyword)

    # 设置查询音乐页面
    def searchMusicBykeywordI(self, keyword):
        self.menus.resetComponents()
        self.pages.setCurrentPage(MenuType.SEARCH.value)
        self.pages.keywordSearchWidget.searchMusicBykeyword(keyword)

    # 设置页面 用于导航栏
    def setPageCurrentIndexI(self, index):
        self.menus.setCurrentIndexI(index)
        self.pages.setCurrentPage(index)

    # 操作recodeStack数据结构
    def recodeStackHandle(self, index, tag=None):
        recodeStack.insert(index, tag)
        # 若为第一次加入 则不设置按钮状态
        if not self.backwardButtonFirst:
            globalSignal.backwardStatusSignal.emit(False)
            globalSignal.forwardStatusSignal.emit(True)
        else:
            self.backwardButtonFirst = False
