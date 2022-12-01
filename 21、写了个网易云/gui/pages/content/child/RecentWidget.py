# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import *

from bean.MusicList import MusicList
from dao.Redis import redis
from gui.components.content.ArtistWidget import ArtistWidget
from gui.components.content.FavourDownloadWidget import FavourDownloadWidget
from gui.components.content.LastestLabel import LastestLabel
from gui.components.content.Table import Table
from gui.components.content.TagWidget import TagWidget
from gui.pages.GlobalSignal import globalSignal


class RecentWidget(TagWidget):

    def __init__(self, tag):
        super(RecentWidget, self).__init__(tag)

        self.initStyle()
        self.initUI()

    def initStyle(self):
        style = """
        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        headerLabels = ['音乐标题', '歌手', '播放时间']
        self.table = Table(headerLabels)
        self.table.setHorizontalHeaderLabels(headerLabels)
        layout.addWidget(self.table)

        # 选中事件
        self.table.doubleClicked.connect(lambda event: globalSignal.playMusic.emit(self.recentMusicList[event.row()]))

    def display(self):
        self.recentMusicList = redis.getValue('recentMusicList', MusicList())
        n = self.recentMusicList.length()
        self.table.setRowCount(n)
        for i in range(n):
            favourDownloadWidget = FavourDownloadWidget(i, self.recentMusicList[i])
            self.table.setCellWidget(i, 0, favourDownloadWidget)

            artistWidget = ArtistWidget(self.recentMusicList[i].artists)
            self.table.setCellWidget(i, 1, artistWidget)

            lastTime = LastestLabel(self.recentMusicList[i].lastestTime)
            self.table.setCellWidget(i, 2, lastTime)
