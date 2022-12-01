# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.common.Button import Button
from gui.components.common.Loading import Loading
from gui.components.content.TagWidget import TagWidget

import qtawesome as qta

from gui.pages.GlobalSignal import globalSignal
from gui.utils.Spider import getPixmapByUrl
from resolver.SpiderResolver import getMusicListByIdResolver
from spider.ListIds import ListIds


class FindMusicWidget(TagWidget):
    finishCount = 0

    def __init__(self, tag):
        super(FindMusicWidget, self).__init__(tag)

        self.resize(800, 600)
        self.initStyle()
        self.initUI()

    def initStyle(self):
        style = """
            QPushButton{
                border:none;
            }
        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        self.loading = Loading()
        self.layout().addWidget(self.loading, 1, 1)

        count = 0
        for item in ListIds:
            widget = TagWidget(item.value)
            widget.playMusicListSignal.connect(self.playMusicList)
            widget.displayMusicListSignal.connect(self.displayMusicList)
            widget.finish.connect(self.loadStateMonitor)
            self.layout().addWidget(widget, count // 3, count % 3, alignment=Qt.AlignHCenter | Qt.AlignVCenter)
            widget.hide()
            count += 1

    def playMusicList(self, music):
        globalSignal.playMusicList.emit(music)

    def displayMusicList(self, music):
        globalSignal.displayMusicList.emit(music)

    def loadStateMonitor(self):
        self.finishCount += 1
        # 已全部加载完成
        if self.finishCount == 9:
            self.loading.hide()
            for i in range(self.layout().count()):
                component = self.layout().itemAt(i).widget()
                if isinstance(component, TagWidget):
                    component.show()


class TagWidget(Button):
    MIN_WIDTH = 220
    MIN_HEIGHT = 220

    playMusicListSignal = pyqtSignal(list)
    displayMusicListSignal = pyqtSignal(list)

    # 检测是否加载完成
    finish = pyqtSignal()

    def __init__(self, id):
        super(TagWidget, self).__init__()

        # 异步加载数据
        self.thread = LoadMusicListThread(id)
        self.thread.finish.connect(self.finishLoad)
        self.thread.start()

        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.setIconSize(QSize(self.MIN_WIDTH, self.MIN_HEIGHT))
        self.clicked.connect(lambda: self.displayMusicListSignal.emit(self.musicList))
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.play = QPushButton()
        self.play.setCursor(QCursor(Qt.PointingHandCursor))
        self.play.setIcon(qta.icon('fa.play-circle-o', color='#D73535'))
        self.play.setIconSize(QSize(60, 60))

        self.play.clicked.connect(lambda: threading.Thread(self.playMusicListSignal.emit(self.musicList)))
        layout.addWidget(self.play)
        self.play.hide()

        self.mouseEnter.connect(lambda: self.showPlay(True))
        self.mouseLeave.connect(lambda: self.showPlay(False))

    def showPlay(self, show):
        if show:
            self.play.show()
        else:
            self.play.hide()

    def finishLoad(self, data):
        threading.Thread(target=self.setCover,
                         args=[data.get('coverImgUrl')]).start()
        self.musicList = data.get('musicList')

    def setCover(self, url):
        self.setIcon(QIcon(getPixmapByUrl(url)))
        self.finish.emit()


# 异步加载歌单数据
class LoadMusicListThread(QThread):
    finish = pyqtSignal(dict)

    # 榜单类型
    def __init__(self, id):
        super(LoadMusicListThread, self).__init__()
        self.id = id

    def run(self):
        data = getMusicListByIdResolver(self.id)
        self.finish.emit(data)


if __name__ == '__main__':
    app = QApplication([])
    window = FindMusicWidget(1)
    window.show()
    app.exec_()
