# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from bean.MusicList import MusicList
from bean.Thread import Thread
from dao.Redis import redis
from gui.components.content.ArtistWidget import ArtistWidget
from gui.components.content.FavourDownloadWidget import FavourDownloadWidget
from gui.components.content.HoverButton import HoverButton
from gui.components.content.LastestLabel import LastestLabel
from gui.components.content.Table import Table
from gui.components.content.TagWidget import TagWidget
from gui.pages.GlobalSignal import globalSignal
from resolver.SpiderResolver import getMusicUrlResolver, getMusicUrlSizeResolver
from setting.SystemVariables import variables
from spider.Download import download, downloadMusic
from gui.utils.TimeFormatter import getTimeStamp


class DownloadWidget(TagWidget):

    def __init__(self, tag):
        super(DownloadWidget, self).__init__(tag)

        self.initParam()
        self.initStyle()
        self.initUI()
        # 绑定全局信号
        globalSignal.downloadMusic.connect(self.downloadMusic)

    def initParam(self):
        # 获取下载路径
        self.downloadPath = variables.MUSIC_DOWNLOAD_PATH
        self.downloadMusicList = redis.getValue("downloadMusicList", MusicList())

    def initStyle(self):
        style = """

        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        headerLabels = ['音乐标题', '歌手', '专辑', '大小', '下载时间']
        self.table = Table(headerLabels)
        self.table.setHorizontalHeaderLabels(headerLabels)
        layout.addWidget(self.table)

        self.table.doubleClicked.connect(lambda event: globalSignal.playMusic.emit(self.downloadMusicList[event.row()]))

    def display(self):
        self.downloadMusicList = redis.getValue("downloadMusicList", MusicList())
        n = self.downloadMusicList.length()
        self.table.setRowCount(n)
        for i in range(n):
            favourDownloadWidget = FavourDownloadWidget(i, self.downloadMusicList[i], showFavourBtn=False,
                                                        showDownloadBtn=False)
            self.table.setCellWidget(i, 0, favourDownloadWidget)

            artistWidget = ArtistWidget(self.downloadMusicList[i].artists)
            self.table.setCellWidget(i, 1, artistWidget)

            albumBtn = HoverButton(inActiveColor='#B4B4B4', activeColor='#6A6B6B', text=self.downloadMusicList[i].album,
                                   tag=self.downloadMusicList[i].album)
            albumBtn.tagSignal.connect(lambda album: globalSignal.keywordSignal.emit(album))
            self.table.setCellWidget(i, 2, albumBtn)

            sizeLabel = QLabel()
            sizeLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            sizeLabel.setText(str(round(self.downloadMusicList[i].size / (1024 * 1024), 2)) + "MB")
            self.table.setCellWidget(i, 3, sizeLabel)

            downloadTime = LastestLabel(self.downloadMusicList[i].downloadTime)
            self.table.setCellWidget(i, 4, downloadTime)

    def downloadMusic(self, music):
        music.downloadTime = getTimeStamp()
        params = getMusicUrlSizeResolver(music.id)
        url = params.get('url')
        music.size = params.get('size')
        self.download = Thread(downloadMusic, url, self.downloadPath, music.name)
        self.download.start()
        self.downloadMusicList.add(music)
