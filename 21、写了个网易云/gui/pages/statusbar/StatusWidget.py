# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from bean.Async import asynchronous
from gui.components.common.CommonButton import CommonButton
from gui.pages.GlobalSignal import globalSignal
from gui.utils.ImgConverter import QIcon
from gui.utils.Path import getPwd
from gui.utils.TimeFormatter import getTimeStamp
from resolver.SpiderResolver import getAvatarByIdResolver
from setting.SystemVariables import variables
from spider.Download import download


class StatusWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.initStyle()
        self.initUI()

    def initStyle(self):
        style = """
            QPushButton{
                border:none;
            }
            #coverImg{
                margin:0 8px;
            }
            #name{
                font-size:18px;
            }
            #name,#favour,#artist{
                text-align:left;                
            }
            #artist{
                font-size:14px;
                font-family:宋体;
            }
            
        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.coverImg = CommonButton()
        self.coverImg.setObjectName("coverImg")
        self.coverImg.setIconSize(QSize(60, 60))
        layout.addWidget(self.coverImg, 0, 0, 0, 1)

        self.name = CommonButton()
        self.name.setObjectName("name")
        layout.addWidget(self.name, 0, 1)

        self.favour = CommonButton(color='red')
        self.favour.setObjectName("favour")
        self.favour.clicked.connect(self.favourMusic)
        layout.addWidget(self.favour, 0, 2)

        self.artists = QWidget()
        artistsLayout = QHBoxLayout()
        artistsLayout.setContentsMargins(0, 0, 0, 0)
        self.artists.setLayout(artistsLayout)
        layout.addWidget(self.artists, 1, 1, 1, 2)

    def favourMusic(self):
        self.favorite = not self.favorite
        self.setFavour(self.favorite)
        # 触发信号

    def setFavour(self, favorite):
        if (favorite):
            self.favour.resetIconName('heart')
        else:
            self.favour.resetIconName('heart-o')

    def display(self, music):
        # 异步
        self.setCover(music)

        self.name.setText(music.name)
        self.favorite = music.favorite
        self.setFavour(self.favorite)

        # 移除所有
        for i in range(self.artists.layout().count()):
            component = self.artists.layout().itemAt(i).widget()
            if isinstance(component, CommonButton) or isinstance(component, QLabel):
                component.deleteLater()
        if music.artists != None:
            for i in range(len(music.artists)):
                artist = CommonButton(music.artists[i], tag=i)
                artist.setObjectName("artist")
                artist.tagSignal.connect(lambda tag: globalSignal.keywordSignal.emit(music.artists[tag]))
                self.artists.layout().addWidget(artist)
        else:
            self.artists.layout().addWidget(QLabel("未知艺术家"))

        if music.filePath != None:
            self.favour.hide()

    @asynchronous
    def setCover(self, music):
        if music.path != None and os.path.isfile(music.path):
            self.coverImg.setIcon(QIcon(music.path))
        else:
            if music.avatar == None and music.avatarId != None:
                music.avatar = getAvatarByIdResolver(music.avatarId)
            if music.avatar != None:
                # 下载图片并缓存
                music.path = download(music.avatar, getPwd(), music.name + "_" + str(music.id))
                self.coverImg.setIcon(QIcon(music.path))
            else:
                if variables.MUSIC_COVER_PATH == None or not os.path.isfile(variables.MUSIC_COVER_PATH):
                    variables.MUSIC_COVER_PATH = download(variables.MUSIC_COVER_URL, getPwd(),
                                                          'MUSIC_COVER_PATH' + "_" + str(getTimeStamp()))
                self.coverImg.setIcon(QIcon(variables.MUSIC_COVER_PATH))
