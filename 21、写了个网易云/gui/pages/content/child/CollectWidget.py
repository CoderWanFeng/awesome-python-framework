# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from bean.MusicList import MusicList
from dao.Redis import redis
from gui.components.content.ArtistWidget import ArtistWidget
from gui.components.content.FavourDownloadWidget import FavourDownloadWidget
from gui.components.content.HoverButton import HoverButton
from gui.components.content.Table import Table
from gui.components.content.TagWidget import TagWidget
from gui.pages.GlobalSignal import globalSignal


class CollectWidget(TagWidget):

    def __init__(self, tag):
        super(CollectWidget, self).__init__(tag)

        self.initStyle()
        self.initUI()

    def initStyle(self):
        style = """

        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        headerLabels = ['音乐标题', '歌手', '专辑']
        self.table = Table(headerLabels)
        self.table.setHorizontalHeaderLabels(headerLabels)
        layout.addWidget(self.table)

        # 选中事件
        self.table.doubleClicked.connect(lambda event: globalSignal.playMusic.emit(self.musicList[event.row()]))

    def display(self):
        self.favoriteMusicList = redis.getValue('favoriteMusicList', MusicList())
        n = self.favoriteMusicList.length()
        self.table.setRowCount(n)
        for i in range(n):
            favourDownloadWidget = FavourDownloadWidget(i, self.favoriteMusicList[i])
            self.table.setCellWidget(i, 0, favourDownloadWidget)

            artistWidget = ArtistWidget(self.favoriteMusicList[i].artists)
            self.table.setCellWidget(i, 1, artistWidget)

            albumBtn = HoverButton(inActiveColor='#B4B4B4', activeColor='#6A6B6B', text=self.favoriteMusicList[i].album,
                                   tag=self.favoriteMusicList[i].album)
            albumBtn.tagSignal.connect(lambda album: globalSignal.keywordSignal.emit(album))
            self.table.setCellWidget(i, 2, albumBtn)
