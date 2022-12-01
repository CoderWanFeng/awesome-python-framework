# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from PyQt5.QtCore import Qt

from bean.MusicList import MusicList
from dao.Redis import redis
from gui.pages.statusbar.ControlWidget import ControlWidget
from gui.pages.statusbar.MusicPlayer import MusicPlayer
from gui.pages.statusbar.StatusWidget import StatusWidget
from gui.utils.TimeFormatter import getTimeStamp


class StatusBar(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedHeight(95)
        self.setCursor(QCursor(Qt.ArrowCursor))

        self.initStyle()
        self.initUI()
        self.preload()

    def initStyle(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        style = """
        StatusBar{
            background-color: #ffffff;
        }
        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.musicBar = StatusWidget()
        self.musicBar.setFixedWidth(220)
        layout.addWidget(self.musicBar)

        layout.addStretch(1)

        self.musicPlayer = MusicPlayer()
        self.musicPlayer.setFixedWidth(565)
        layout.addWidget(self.musicPlayer)

        layout.addStretch(1)

        controlBar = ControlWidget()
        controlBar.volumnSignal.connect(self.setVolumn)
        controlBar.setFixedWidth(220)
        layout.addWidget(controlBar)

    def setVolumn(self, value):
        self.musicPlayer.setVolume(value)

    # 预加载
    def preload(self):
        self.songs = redis.getValue('songs', MusicList())
        self.recentMusicList = redis.getValue("recentMusicList", MusicList())
        music = self.songs.getCurrentMusic()
        if music:
            self.musicBar.display(music)
            self.musicPlayer.prePlay(music)

    # 更新最近播放
    def updateRecentMusicList(self, music):
        music.lastestTime = getTimeStamp()
        for item in self.recentMusicList:
            if music.id == item.id:
                break
        self.recentMusicList.add(music)

    def playMusic(self, music):
        self.updateRecentMusicList(music)
        self.musicBar.display(music)
        self.musicPlayer.play(music)

    def playLocalMusic(self, music):
        self.musicBar.display(music)
        self.musicPlayer.playLocalMusic(music)
