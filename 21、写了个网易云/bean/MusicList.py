# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH

# 音乐列表 - 数据结构
class MusicList(list):
    # 指针
    point = -1

    def __init__(self):
        super(MusicList, self).__init__()

    def add(self, music):
        self.point += 1
        self.append(music)

    def insertBatch(self, musicList):
        if len(musicList) > 0:
            # 更新位置
            self.point = len(self)
            self += musicList

    def getCurrentMusic(self):
        if len(self) > 0:
            return self[self.point]
        else:
            return None

    def forward(self):
        self.point -= 1
        mod = len(self)
        self.point = (self.point + mod) % mod
        return self[self.point]

    def backward(self):
        self.point += 1
        self.point %= len(self)
        return self[self.point]

    def clear(self):
        self.point = -1
        self = []

    def isBegin(self):
        return self.point == 0

    def isDeadline(self):
        return self.point == len(self) - 1

    def length(self):
        return len(self)

    def extrapolate(self, music):
        self.insert(0, music)
