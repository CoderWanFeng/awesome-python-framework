# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
# 时间转换
import math
import time
from datetime import datetime


def MSToTime(ms):
    return SToTime(ms / 1000)


def SToTime(s):
    minute = int(s // 60)
    if minute < 10:
        minute = '0' + str(minute)
    second = math.floor(s % 60)
    if second < 10:
        second = '0' + str(second)
    return str(minute) + ":" + str(second)


def getTimeStamp():
    return math.floor(time.time())


def timeStamptoTime(timeStamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp))

