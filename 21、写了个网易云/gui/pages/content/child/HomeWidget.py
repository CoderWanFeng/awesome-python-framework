# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from bean.Music import Music
from dao.Redis import redis
from gui.components.content.Table import Table
from gui.components.content.TagWidget import TagWidget
from gui.pages.GlobalSignal import globalSignal


class HomeWidget(TagWidget):
    musicList = []

    def __init__(self, tag):
        super(HomeWidget, self).__init__(tag)
        self.initParams()
        self.initStyle()
        self.initUI()

    def initParams(self):
        self.localMusicDirs = redis.getValue('localMusicDirs', [])

    def initStyle(self):
        style = """
            QPushButton{
            }
        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        self.combox = QComboBox()
        self.combox.currentIndexChanged[str].connect(self.handle)
        layout.addWidget(self.combox, 0, 0, 1, 3)

        button = QPushButton("选择目录")
        button.clicked.connect(self.selectMusicDir)
        layout.addWidget(button, 0, 3)

        headerLabels = ["歌曲名称"]
        self.table = Table(headerLabels)
        self.table.setHorizontalHeaderLabels(headerLabels)
        self.table.doubleClicked.connect(lambda event: globalSignal.playLocalMusic.emit(self.musicList[event.row()]))
        layout.addWidget(self.table, 1, 0, 1, 4)

        for dir in self.localMusicDirs:
            self.combox.addItem(dir)

    def handle(self, dirPath):
        self.loadMusicList(dirPath)
        self.showMusicList()

    # 选择目录
    def selectMusicDir(self):
        path = QFileDialog.getExistingDirectory(self, "选择目录")
        if path:
            for i in range(self.combox.count()):
                if self.combox.itemText(i) == path:
                    return
            self.localMusicDirs.append(path)
            self.combox.addItem(path)

    # 加载指定文件夹下的音乐文件
    def loadMusicList(self, dir):
        self.musicList = []
        format = ['mp3', 'm4a', 'flac', 'wav', 'ogg']
        for song in os.listdir(dir):
            if song.split('.')[-1] in format:
                self.musicList.append(
                    Music(name=song, filePath=os.path.join(dir, song).replace('\\', '/')))

    def showMusicList(self):
        self.table.setRowCount(len(self.musicList))
        for index in range(len(self.musicList)):
            self.table.setItem(index, 0, QTableWidgetItem(self.musicList[index].name))

        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                self.table.item(i, j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
