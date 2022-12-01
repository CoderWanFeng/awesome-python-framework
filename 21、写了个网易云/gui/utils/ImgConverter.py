# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
# 把图片变为圆形
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def ToCircleImg(url, width, height, parent):
    originImg = QPixmap(url)
    newImg = QPixmap(width, height)
    newImg.fill(Qt.transparent)
    painter = QPainter(newImg)
    painter.begin(parent)
    # 一个是平滑，一个是缩放保持比例
    painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
    path = QPainterPath()
    path.addEllipse(0, 0, width, height);  # 绘制椭圆
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, width, height, originImg)
    painter.end()
    return newImg
