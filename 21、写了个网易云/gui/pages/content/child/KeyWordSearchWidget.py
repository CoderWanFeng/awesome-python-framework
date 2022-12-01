# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import *

from gui.components.common.Loading import Loading
from gui.components.content.ArtistWidget import ArtistWidget
from gui.components.content.FavourDownloadWidget import FavourDownloadWidget
from gui.components.content.HoverButton import HoverButton
from gui.components.content.Table import Table
from gui.components.content.TagWidget import TagWidget
from gui.pages.GlobalSignal import globalSignal
from resolver.SpiderResolver import getMusicListByKeywordResolver
from bean.Thread import Thread


class KeyWordSearchWidget(TagWidget):

    def __init__(self, tag):
        super(KeyWordSearchWidget, self).__init__(tag)

        self.initParams()
        self.initStyle()
        self.initUI()

    def initParams(self):
        self.count = 5

    def initStyle(self):
        style = """

        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        # 加载效果
        self.loading = Loading()
        self.loading.hide()
        layout.addWidget(self.loading)

        # 信息展示
        headerLabels = ['音乐标题', '歌手', '专辑']
        self.table = Table(headerLabels)
        self.table.setHorizontalHeaderLabels(headerLabels)
        self.table.hide()
        layout.addWidget(self.table)

        # 选中事件
        self.table.doubleClicked.connect(lambda event: globalSignal.playMusic.emit(self.musicList[event.row()]))

    def searchMusicBykeyword(self, keyword):
        # 每次查询初始化参数
        self.pages = 1
        self.musicList = []
        self.keyword = keyword
        self.nextPage()

    def callback(self, data):
        start = len(self.musicList)
        self.musicList += data
        n = len(data)
        self.table.setRowCount(n)
        if n < self.count:
            # 修改下一页为不可点击
            pass
        for i in range(n):
            # 对查询结果进行遍历
            favourDownloadWidget = FavourDownloadWidget(i, data[i])
            self.table.setCellWidget(i, 0, favourDownloadWidget)

            artistWidget = ArtistWidget(data[i].artists)
            self.table.setCellWidget(i, 1, artistWidget)

            albumBtn = HoverButton(inActiveColor='#B4B4B4', activeColor='#6A6B6B', text=data[i].album,
                                   tag=data[i].album)
            albumBtn.tagSignal.connect(lambda album: globalSignal.keywordSignal.emit(album))
            self.table.setCellWidget(i, 2, albumBtn)

            self.loading.hide()
            self.table.show()

    def nextPage(self):
        self.table.hide()
        self.loading.show()

        self.thread = Thread(getMusicListByKeywordResolver, self.count, self.pages, self.keyword)
        self.thread.finish.connect(self.callback)
        self.thread.start()
