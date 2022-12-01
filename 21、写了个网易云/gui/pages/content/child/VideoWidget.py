# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
import wordcloud
from bean.Async import asynchronous
from dao.Redis import redis
from gui.components.content.TagWidget import TagWidget


class VideoWidget(TagWidget):

    def __init__(self, tag):
        super(VideoWidget, self).__init__(tag)

        self.initParams()
        self.initStyle()
        self.initUI()

        self.wordcloudGenerator = wordcloud.WordCloud(font_path='msyh.ttc', background_color='white')

    def initParams(self):
        self.words = redis.getValue('words', [])

    def initStyle(self):
        style = """

        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.img = QLabel()
        self.img.setScaledContents(True)
        layout.addWidget(self.img)

    @asynchronous
    def display(self):
        if len(self.words) > 0:
            self.wordcloudGenerator.generate_from_frequencies(dict(self.words))
            # self.wordcloudGenerator.to_image()
            # self.img.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
            self.wordcloudGenerator.to_file("abc.jpg")
            self.img.setPixmap(QPixmap("abc.jpg"))
