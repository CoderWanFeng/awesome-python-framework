# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from gui.components.content.HoverButton import HoverButton

# 音乐标题栏按钮
from gui.pages.GlobalSignal import globalSignal


class ArtistWidget(QWidget):

    def __init__(self, artists):
        super(ArtistWidget, self).__init__()
        self.artists = artists
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        for i in range(len(self.artists)):
            btn = HoverButton(inActiveColor='#B4B4B4', activeColor='#6A6B6B', text=self.artists[i], tag=i)
            btn.tagSignal.connect(self.handle)
            layout.addWidget(btn)

    def handle(self, index):
        globalSignal.keywordSignal.emit(self.artists[index])
