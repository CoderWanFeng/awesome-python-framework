# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
import requests
from PyQt5.QtGui import *


def getPixmapByUrl(url):
    data = requests.get(url).content
    return QPixmap.fromImage(QImage.fromData(data))
