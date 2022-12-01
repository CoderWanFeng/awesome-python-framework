# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication

from gui.components.common.CommonButton import CommonButton


class MusicItem(QWidget):

    def __init__(self, id, name, artist, album, url, avatar, lyric):
        super(MusicItem, self).__init__()

        self.initStyle()
        self.initUI(id, name, artist, album, url, avatar, lyric)

    def initStyle(self):
        style = """
            CommonButton{
                border:none;
            }
        """
        self.setStyleSheet(style)

    def initUI(self, id, name, artist, album, url, avatar, lyric):
        layout = QHBoxLayout()
        self.setLayout(layout)

        id = QLabel(str(id))
        layout.addWidget(id)

        layout.addStretch(2)

        name = QLabel(name)
        layout.addWidget(name)

        layout.addStretch(1)

        artist = CommonButton(artist)
        layout.addWidget(artist)

        layout.addStretch(1)

        album = CommonButton(album)
        layout.addWidget(album)


if __name__ == '__main__':
    app = QApplication([])
    window = MusicItem(1, '十七岁', 'wo1', '专辑', 'www.baidu.com', 'aaa', 'bbb')
    window.show()
    app.exec_()
