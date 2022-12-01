# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout


# 加载组件
# 注意！ .gif 图片路径
class Loading(QWidget):

    def __init__(self, *args):
        super(Loading, self).__init__(*args)

        self.setFixedSize(100, 40)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        img = QLabel()
        gif = QMovie('../../resource/img/loading.gif')
        img.setMovie(gif)
        layout.addWidget(img)
        gif.start()

        text = QLabel("加载中")
        text.setStyleSheet("font-weight:bold;")
        layout.addWidget(text)
