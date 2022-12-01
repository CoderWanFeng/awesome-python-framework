# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from bean.Async import asynchronous
from bean.MusicList import MusicList
from gui.components.common.HSeparateLine import HSeparateLine
from gui.pages.content.Content import Content
from gui.pages.GlobalSignal import globalSignal
from gui.pages.navbar.NavBar import NavBar
from gui.pages.statusbar.StatusBar import StatusBar
from dao.Redis import redis
from resolver.SpiderResolver import getMusicListByKeywordResolver


class Window(QWidget):
    # 窗体的最小宽高
    WINDOW_MIN_WIDTH = 1275
    WINDOW_MIN_HEIGHT = 835
    # 窗口边框宽度
    WINDOW_SHADOW_MARGIN = 20
    # 窗口拖拽标记
    drag = False
    dragValid = False
    flag = -1

    def __init__(self):
        super(Window, self).__init__()

        # 窗口基本参数配置
        self.setMinimumSize(self.WINDOW_MIN_WIDTH + 2 * self.WINDOW_SHADOW_MARGIN,
                            self.WINDOW_MIN_HEIGHT + 2 * self.WINDOW_SHADOW_MARGIN)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

        self.initParams()
        self.initUI()
        # 全局信号处理
        self.globalSignalHandle()

    def initParams(self):
        size = redis.getValue('size', QSize(self.WINDOW_MIN_WIDTH, self.WINDOW_MIN_HEIGHT))
        self.resize(size)
        pos = QPoint((QApplication.desktop().width() - size.width()) / 2,
                     (QApplication.desktop().height() - size.height()) / 2)
        self.isMaximize = redis.getValue('isMaximize', 0)

        # 歌曲相关
        # 当前正在播放的歌单
        self.songs = redis.getValue("songs", MusicList())
        # 最近播放歌单 音乐标题 歌手 播放时间 清空列表
        self.recentMusicList = redis.getValue("recentMusicList", MusicList())
        # 收藏歌单
        self.favoriteMusicList = redis.getValue("favoriteMusicList", MusicList())
        # 下载歌单
        self.downloadMusicList = redis.getValue("downloadMusicList", MusicList())

        self.words = redis.getValue('words', [])

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        # 是否最大化
        if self.isMaximize:
            self.setLayoutContentsMargins(0)
            self.showMaximized()
        else:
            self.setLayoutContentsMargins(self.WINDOW_SHADOW_MARGIN)

        # 窗口边框绘制
        border = QGraphicsDropShadowEffect()
        border.setOffset(0, 0)
        border.setColor(QColor("#444444"))
        border.setBlurRadius(self.WINDOW_SHADOW_MARGIN)
        self.setGraphicsEffect(border)

        self.navBar = NavBar()
        self.navBar.setMaximumHeight(75)
        self.navBar.moveSignal.connect(self.moveSignalHandle)
        self.navBar.minimizeSignal.connect(self.showMinimized)
        self.navBar.maximizeSignal.connect(self.maximizeSignalHandle)
        self.navBar.restoreSignal.connect(self.restoreSignalHandle)
        self.navBar.closeSignal.connect(self.closeSignalHandle)

        layout.addWidget(self.navBar)

        self.content = Content()
        layout.addWidget(self.content)

        separateLine = HSeparateLine()
        separateLine.setStyleSheet("background:#F6F6F7;border:1px solid #F6F6F7")
        layout.addWidget(separateLine)

        self.statusBar = StatusBar()
        self.statusBar.setMaximumHeight(100)
        layout.addWidget(self.statusBar)

    def globalSignalHandle(self):
        globalSignal.playMusicList.connect(self.playMusicList)
        globalSignal.playPreMusic.connect(self.playPreMusic)
        globalSignal.playNextMusic.connect(self.playNextMusic)
        globalSignal.keywordSignal.connect(lambda keyword: self.content.searchMusicBykeyword(keyword))
        globalSignal.playMusic.connect(self.playMusic)
        globalSignal.favourMusic.connect(self.favourMusic)
        globalSignal.playLocalMusic.connect(self.playLocalMusic)
        globalSignal.playStyleMusic.connect(self.playStyleMusic)

    # 播放歌单
    def playMusicList(self, musicList):
        self.songs.clear()
        self.songs.insertBatch(musicList)
        # 添加至最近播放音乐列表
        music = self.songs.getCurrentMusic()
        self.statusBar.playMusic(music)

    def playPreMusic(self):
        music = self.songs.forward()
        self.statusBar.playMusic(music)

    def playNextMusic(self):
        music = self.songs.backward()
        self.statusBar.playMusic(music)

    def playMusic(self, music):
        self.statusBar.playMusic(music)

    def favourMusic(self, music):
        if music.favorite:  # 从未收藏 变为 已经收藏
            self.favoriteMusicList.extrapolate(music)
        else:  # 从已经收藏 变为未收藏
            for i in range(self.favoriteMusicList.length()):
                if self.favoriteMusicList[i].id == music.id:
                    del self.favoriteMusicList[i]
            self.content.pages.collectWidget.display()

    def playLocalMusic(self, music):
        self.statusBar.playLocalMusic(music)

    # 窗口相关
    # 设置边框宽度 注：请确保已为窗口设置布局
    def setLayoutContentsMargins(self, width):
        self.layout().setContentsMargins(width, width, width, width)

    # 窗口移动
    def moveSignalHandle(self, pos):
        self.move(QPoint(pos.x() - self.WINDOW_SHADOW_MARGIN, pos.y() - self.WINDOW_SHADOW_MARGIN))

    # 窗口最大化
    def maximizeSignalHandle(self):
        self.setLayoutContentsMargins(0)
        self.isMaximize = 1
        self.showMaximized()

    # 窗口还原
    def restoreSignalHandle(self):
        self.setLayoutContentsMargins(self.WINDOW_SHADOW_MARGIN)
        self.isMaximize = 0
        self.showNormal()

    # 关闭窗口
    def closeSignalHandle(self):
        if self.pos().y() + self.size().height() > QApplication.desktop().height() or self.pos().y() < 0 or self.pos().x() < 0 or self.pos().x() + self.size().width() > QApplication.desktop().width():
            redis.setValue('size', None)
        else:
            redis.setValue('size', QSize(self.size().width(), self.size().height()))
        redis.setValue('isMaximize', self.isMaximize)
        redis.serialize()
        self.close()

    # 窗口大小可拖拽
    def mousePressEvent(self, event):
        self.drag = True
        self.originPos = self.pos()

    def mouseMoveEvent(self, event):
        distance = 0
        factor = self.WINDOW_SHADOW_MARGIN / 2
        if self.isMaximize:
            return

        if self.dragValid == False:
            if event.globalPos().x() > (self.pos().x() + self.width() - self.WINDOW_SHADOW_MARGIN + distance) \
                    and event.globalPos().x() - (
                    self.pos().x() + self.width() - self.WINDOW_SHADOW_MARGIN + distance) < factor:
                if event.globalPos().y() < (self.WINDOW_SHADOW_MARGIN + self.pos().y() - distance) and (
                        self.WINDOW_SHADOW_MARGIN + self.pos().y() - distance) - event.globalPos().y() < factor:
                    self.flag = 1  # 右上
                    self.setCursor(QCursor(Qt.SizeBDiagCursor))
                elif event.globalPos().y() > (self.pos().y() + self.height() - self.WINDOW_SHADOW_MARGIN + distance) and \
                        event.globalPos().y() - (
                        self.pos().y() + self.height() - self.WINDOW_SHADOW_MARGIN + distance) < factor:
                    self.flag = 2  # 右下
                    self.setCursor(QCursor(Qt.SizeFDiagCursor))
                elif event.globalPos().y() >= (
                        self.pos().y() + self.WINDOW_SHADOW_MARGIN) and event.globalPos().y() <= (
                        self.pos().y() + self.height() - self.WINDOW_SHADOW_MARGIN):
                    self.flag = 0  # 右0
                    self.setCursor(QCursor(Qt.SizeHorCursor))
                else:
                    pass
            elif event.globalPos().x() < (self.pos().x() + self.WINDOW_SHADOW_MARGIN - distance) and (
                    self.pos().x() + self.WINDOW_SHADOW_MARGIN - distance) - event.globalPos().x() < factor:
                if event.globalPos().y() < (self.WINDOW_SHADOW_MARGIN + self.pos().y() - distance) and (
                        self.WINDOW_SHADOW_MARGIN + self.pos().y() - distance) - event.globalPos().y() < factor:
                    self.flag = 3  # 左上
                    self.setCursor(QCursor(Qt.SizeFDiagCursor))
                elif event.globalPos().y() > (self.pos().y() + self.height() - self.WINDOW_SHADOW_MARGIN + distance) and \
                        event.globalPos().y() - (
                        self.pos().y() + self.height() - self.WINDOW_SHADOW_MARGIN + distance) < factor:
                    self.flag = 4  # 左下
                    self.setCursor(QCursor(Qt.SizeBDiagCursor))
                else:
                    pass
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

        if Qt.LeftButton and self.drag:
            self.dragValid = True
            if self.flag == 0:  # 右边拖动
                self.resize(QSize(event.globalPos().x() - self.pos().x() + self.WINDOW_SHADOW_MARGIN, self.height()))
            elif self.flag == 1:  # 右上拖动
                self.resize(QSize(event.globalPos().x() - self.pos().x() + self.WINDOW_SHADOW_MARGIN,
                                  self.height() + self.pos().y() + self.WINDOW_SHADOW_MARGIN - event.globalPos().y()))
                y = self.pos().y() - self.pos().y() - self.WINDOW_SHADOW_MARGIN + event.globalPos().y()
                if y > self.originPos.y():
                    y = self.originPos.y()
                self.move(self.x(), y)
            elif self.flag == 2:  # 右下拖动
                self.resize(QSize(event.globalPos().x() - self.pos().x() + self.WINDOW_SHADOW_MARGIN,
                                  self.height() + event.globalPos().y() - self.pos().y() - self.height() + self.WINDOW_SHADOW_MARGIN))
            elif self.flag == 3:  # 左上拖动
                self.resize(QSize(self.width() + (self.pos().x() + self.WINDOW_SHADOW_MARGIN) - event.globalPos().x(),
                                  self.height() + self.pos().y() + self.WINDOW_SHADOW_MARGIN - event.globalPos().y()))

                x = self.pos().x() - ((self.pos().x() + self.WINDOW_SHADOW_MARGIN) - event.globalPos().x())
                y = self.pos().y() - (self.pos().y() + self.WINDOW_SHADOW_MARGIN - event.globalPos().y())
                if x > self.originPos.x():
                    x = self.originPos.x()
                if y > self.originPos.y():
                    y = self.originPos.y()
                self.move(x, y)
            elif self.flag == 4:  # 左下拖动
                self.resize(QSize(self.width() + (self.pos().x() + self.WINDOW_SHADOW_MARGIN) - event.globalPos().x(),
                                  self.height() + event.globalPos().y() - self.pos().y() - self.height() + self.WINDOW_SHADOW_MARGIN))
                x = self.pos().x() - ((self.pos().x() + self.WINDOW_SHADOW_MARGIN) - event.globalPos().x())
                if x > self.originPos.x():
                    x = self.originPos.x()
                self.move(x, self.pos().y())
            else:
                pass

    def mouseReleaseEvent(self, event):
        self.drag = False
        self.dragValid = False

    @asynchronous
    def playStyleMusic(self):
        self.words.sort(key=lambda x: x[1], reverse=True)
        self.songs.clear()
        self.songs.insertBatch(getMusicListByKeywordResolver(10, 1, self.words[0][0]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

# /storage/emulated/0/Music
