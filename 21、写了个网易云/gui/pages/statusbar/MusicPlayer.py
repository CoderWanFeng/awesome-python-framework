# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
import jieba
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QUrl

from bean.Async import asynchronous
from bean.Excludes import getExcludes
from dao.Redis import redis
from gui.components.common.CommonButton import CommonButton
from gui.components.common.ProgressBar import ProgressBar
from gui.components.content.HoverButton import HoverButton
from gui.pages.GlobalSignal import globalSignal
from gui.pages.statusbar.LyricWidget import LyricWidget
from gui.utils.LyricFormatter import lyricFormatter
from gui.utils.TimeFormatter import MSToTime, SToTime
from resolver.SpiderResolver import getMusicUrlResolver, getLyricByIdResolver, Source


class MusicPlayer(QWidget):
    # 播放器
    player = QMediaPlayer()
    # 播放器状态
    playing = False
    # 连续播放错误歌曲数
    serialErrorCount = 0

    def __init__(self):
        super(MusicPlayer, self).__init__()

        self.initParams()
        self.initStyle()
        self.initUI()

        self.player.durationChanged.connect(self.setDuration)
        self.player.mediaStatusChanged.connect(self.playNextMusicCallBack)

        self.clock = Clock()
        self.clock.call.connect(self.setProgressValue)
        self.clock.call.connect(self.setLyric)

    def initParams(self):
        self.excludes = getExcludes()
        self.words = redis.getValue('words', [])

    def initStyle(self):
        style = """
        QProgressBar{
           border-radius: 5px;
           background-color: #E5E5E5;
        }
        QProgressBar::chunk {
           border-radius: 5px;
           background-color: #FF4E4E;
        }
        QPushButton{
            border:none;
        }
        #schema{
            margin-right:18px;
        }
        #status{
            border-radius:15px;
            width:30px;
            height:30px;
            background-color:#F4F4F4
        }
        #status:hover{
            background-color:#E5E5E5;
        }
        #lyric{
            margin-left:18px;
            font-weight:bold;
        }
        #lyric:hover{
            color:#FF4E4E;
        }
        """
        self.setStyleSheet(style)

    def initUI(self):
        activeColor = '#FF4E4E'
        inActiveColor = '#333333'

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.schema = HoverButton(activeColor=activeColor, inActiveColor=inActiveColor, iconName='heartbeat')
        self.schema.setObjectName("schema")
        self.schema.clicked.connect(globalSignal.playStyleMusic)
        layout.addWidget(self.schema, 0, 0, 1, 3, Qt.AlignRight)

        self.backward = HoverButton(activeColor=activeColor, inActiveColor=inActiveColor, iconName='step-backward')
        self.backward.clicked.connect(self.playPreMusic)
        layout.addWidget(self.backward, 0, 3)

        self.status = HoverButton(activeColor=inActiveColor, inActiveColor=inActiveColor, iconName='play')
        self.status.setObjectName("status")
        self.status.clicked.connect(self.pause)
        layout.addWidget(self.status, 0, 4)

        self.forward = HoverButton(activeColor=activeColor, inActiveColor=inActiveColor, iconName='step-forward')
        self.forward.clicked.connect(self.playNextMusic)
        layout.addWidget(self.forward, 0, 5)

        self.lyric = CommonButton("词")
        self.lyric.setObjectName("lyric")
        self.lyric.clicked.connect(self.showLyricWidget)
        layout.addWidget(self.lyric, 0, 6, 1, 3, Qt.AlignLeft)

        self.current = QLabel("00:00")
        layout.addWidget(self.current, 1, 0, Qt.AlignRight)

        self.progress = ProgressBar()
        self.progress.setFixedHeight(6)  # 设置进度条高度
        self.progress.clicked.connect(self.skip)
        layout.addWidget(self.progress, 1, 1, 1, 7)

        self.total = QLabel()
        layout.addWidget(self.total, 1, 8, Qt.AlignLeft)

        self.lyricWidget = LyricWidget()
        self.lyricWidget.hide()

    # 音乐跳转
    def skip(self, value):
        value = self.duration * value // 1000 * 1000
        self.player.setPosition(value)
        self.clock.reset(value / 1000)
        self.setProgressValue(value / 1000)

    @asynchronous
    def play(self, music):
        self.clock.stop()
        self.clock.reset()

        self.playVO(music)
        self.playing = True
        self.player.play()
        self.status.resetIconName('pause')

    def setDuration(self, duration):
        self.duration = duration
        self.total.setText(MSToTime(self.duration))
        if self.player.mediaStatus() != QMediaPlayer.MediaStatus.LoadedMedia:
            self.clock.start()

    def setProgressValue(self, count):
        self.current.setText(SToTime(count))
        if self.duration > 0:
            # 更新进度条
            self.progress.setValue((count * 1000 * 100 / self.duration))
            self.progress.update()

    def pause(self):
        if self.playing:
            self.status.resetIconName('play')
            self.player.pause()
            self.playing = False
            self.clock.stop()
        else:
            self.status.resetIconName('pause')
            self.playing = True
            mediaStatus = self.player.mediaStatus()
            if mediaStatus == QMediaPlayer.MediaStatus.BufferedMedia or mediaStatus == QMediaPlayer.MediaStatus.LoadedMedia:
                self.clock.start()
                self.player.play()
            else:
                pass

    def setVolume(self, value):
        self.player.setVolume(value)

    def playPreMusic(self):
        self.clock.stop()
        self.clock.reset()
        globalSignal.playPreMusic.emit()

    def playNextMusic(self):
        self.clock.stop()
        self.clock.reset()
        globalSignal.playNextMusic.emit()

    def playNextMusicCallBack(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.clock.stop()
            self.clock.reset()
            globalSignal.playNextMusic.emit()

    @asynchronous
    def prePlay(self, music):
        self.playVO(music)
        self.playing = False
        self.status.resetIconName('play')

    # 歌词展示
    def showLyricWidget(self):
        if self.lyricWidget.isVisible():
            self.lyricWidget.hide()
            self.lyric.setStyleSheet("margin-left:18px;font-weight:bold;color:#000000;:hover{color:#FF4E4E;}")
        else:
            self.lyricWidget.show()
            self.lyric.setStyleSheet("margin-left:18px;font-weight:bold;color:#FF4E4E;")

    def setLyric(self, count):
        if self.lyricText != None:
            text = self.lyricText.get(count)
            if text != None:
                self.lyricWidget.setLyric(text)
        else:
            self.lyricWidget.setLyric("当前歌曲为本地音乐，无歌词！")

    # 预加载播放 与 播放 公共抽取
    def playVO(self, music):
        music.url = getMusicUrlResolver(music.id)
        if music.url == '':
            if self.serialErrorCount < 3:
                print("获取" + music.name + "歌曲链接失败！ 已为您跳转至下一首")
                globalSignal.playNextMusic.emit()
                self.serialErrorCount += 1
            else:
                print("本歌单已连续3首播放失败，请选择其他歌单")
                self.serialErrorCount = 0
            return
        if music.lyricId != None:
            music.lyric = lyricFormatter(getLyricByIdResolver(music.lyricId, music.source))
        else:
            music.lyric = lyricFormatter(getLyricByIdResolver(music.id, Source.Netease_Cloud_Music.value))
        self.frequencyStatistics(music.lyric)
        self.lyricText = music.lyric
        self.player.setMedia(QMediaContent(QUrl(music.url)))

    def playLocalMusic(self, music):
        self.clock.stop()
        self.clock.reset()

        self.lyricText = None
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(music.filePath)))
        self.playing = True
        self.player.play()
        self.status.resetIconName('pause')

    # 根据歌词做频率统计
    def frequencyStatistics(self, lyric):
        lyric = " ".join(lyric.values())
        words = jieba.lcut(lyric)
        temps = {}
        for word in words:
            if len(word) == 1 or word in self.excludes:
                continue
            temps[word] = temps.get(word, 0) + 1
        items = list(temps.items())
        items.sort(key=lambda x: x[1], reverse=True)
        self.words += items[0:10]




class Clock(QTimer):
    call = pyqtSignal(int)
    count = 0

    def __init__(self, interval=1000):
        super(Clock, self).__init__()

        self.setInterval(interval)
        self.timeout.connect(self.handle)

    def reset(self, count=0):
        self.count = count

    def handle(self):
        self.count += 1
        self.call.emit(self.count)
