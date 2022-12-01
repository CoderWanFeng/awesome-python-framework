# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
import re


def lyricFormatter(lyric):
    # 根据换行符分割字符串
    list = lyric.split("\n")
    # 除去无效数据
    del list[0]
    del list[len(list) - 1]

    lyricText = {}

    for i in range(len(list)):
        # 切分为 时间 歌词
        temp = list[i].split(']')
        # 切分 minute 秒 毫秒
        temp[0] = temp[0][1:-1]

        time = re.split('[:.]', temp[0])
        if int(time[2]) > 50:
            time[1] = int(time[1]) + 1
        time = int(time[0]) * 60 + int(time[1])
        lyricText[time] = temp[1]
    return lyricText
