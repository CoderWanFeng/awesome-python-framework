# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
class RecodeStack:
    recodes = []
    ptr = -1

    def __init__(self):
        super(RecodeStack, self).__init__()

    # pageIndex 页面下标
    # tag 附信息
    def insert(self, pageIndex, tag=None):
        self.ptr += 1
        del self.recodes[self.ptr:len(self.recodes)]
        self.recodes.insert(self.ptr, [pageIndex, tag])

    def backward(self):
        self.ptr -= 1
        return self.recodes[self.ptr]

    def forward(self):
        self.ptr += 1
        return self.recodes[self.ptr]

    def isBegin(self):
        return self.ptr == 0

    def isDeadline(self):
        return self.ptr == len(self.recodes) - 1


recodeStack = RecodeStack()
