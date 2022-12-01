# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from bean.MusicList import MusicList
from dao.Redis import redis
from gui.components.content.HoverButton import HoverButton

# 音乐标题栏按钮
from gui.pages.GlobalSignal import globalSignal


class FavourDownloadWidget(QWidget):
    favourSignal = pyqtSignal(int)
    downloadSignal = pyqtSignal(int)

    def __init__(self, index, music, showFavourBtn=True, showDownloadBtn=True):
        super(FavourDownloadWidget, self).__init__()

        self.index = index
        self.music = music
        self.initUI(showFavourBtn, showDownloadBtn)

    def initUI(self, showFavourBtn, showDownloadBtn):
        layout = QHBoxLayout()
        self.setLayout(layout)

        tagLabel = QLabel()
        tagLabel.setStyleSheet("font-weight:bold;")
        tagLabel.setText(self.getText())
        layout.addWidget(tagLabel)

        if showFavourBtn:
            # 判断当前歌曲是否已经收藏
            self.setMusicFavour()
            self.favourBtn = HoverButton()
            self.setFavourBtn()
            self.favourBtn.clicked.connect(self.handle)
            layout.addWidget(self.favourBtn)

        if showDownloadBtn:
            downloadBtn = HoverButton(iconName='download', inActiveColor='#B4B4B4', activeColor='#6A6B6B')
            downloadBtn.clicked.connect(lambda: globalSignal.downloadMusic.emit(self.music))
            layout.addWidget(downloadBtn)

        layout.addStretch(2)

        nameLabel = QLabel()
        nameLabel.setText(self.music.name)
        layout.addWidget(nameLabel)

        layout.addStretch(1)

    def getText(self):
        id = self.index + 1
        if id < 10:
            return '0' + str(id)
        else:
            return str(id)

    def handle(self):
        self.music.favorite = not self.music.favorite
        self.setFavourBtn()
        globalSignal.favourMusic.emit(self.music)

    def setFavourBtn(self):
        if self.music.favorite:
            self.favourBtn.resetIconName('heart')
            self.favourBtn.resetIconColor('#EC4141', '#EC4141')
        else:
            self.favourBtn.resetIconName('heart-o')
            self.favourBtn.resetIconColor('#B4B4B4', '#6A6B6B')

    def setMusicFavour(self):
        self.favoriteMusicList = redis.getValue('favoriteMusicList', MusicList())
        for i in range(self.favoriteMusicList.length()):
            if self.favoriteMusicList[i].id == self.music.id:
                self.music.favorite = True
                return
