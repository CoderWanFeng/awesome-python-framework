# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import pyqtSignal, QObject

from bean.Music import Music


class Signal(QObject):
    # ------------------------------ 搜索相关-----------------------------------#
    # 播放音乐
    playMusic = pyqtSignal(Music)
    # 下载音乐
    downloadMusic = pyqtSignal(Music)
    # 收藏音乐
    favourMusic = pyqtSignal(Music)
    # ------------------------------导航栏相关-----------------------------------#
    # 关键字查询
    keywordSignal = pyqtSignal(str)
    # 根据索引进行页面跳转
    pageIndexSignal = pyqtSignal(int)
    # 设置backward状态
    backwardStatusSignal = pyqtSignal(bool)
    # 设置forward状态
    forwardStatusSignal = pyqtSignal(bool)
    # 用于进退
    keywordSignalI = pyqtSignal(str)
    # ----------------------------发现页面相关信号--------------------------------#
    # 播放音乐列表
    playMusicList = pyqtSignal(list)
    # 跳转到展示音乐列表界面
    displayMusicList = pyqtSignal(list)
    # -------------------------- 音乐播放器相关信号 ----------------------------- #
    # 播放上一首
    playPreMusic = pyqtSignal()
    # 播放下一首
    playNextMusic = pyqtSignal()
    # -------------------------- 本地音乐相关信号 ----------------------------- #
    playLocalMusic = pyqtSignal(Music)

    playStyleMusic = pyqtSignal()

    def __init__(self):
        super(Signal, self).__init__()


globalSignal = Signal()
